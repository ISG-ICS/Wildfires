#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import pickle
from datetime import datetime

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

from satellite_classification.asc2xyz import ASC2XYZ


def export_wildfile_info(wildfire_info_filename):
    wildfire_info_file = open(wildfire_info_filename)
    wildfire_list = []
    flag = 0
    for line in wildfire_info_file:
        if flag == 0:
            flag = 1
            continue
        lat = float(line.split(',')[5])
        long_ = float(line.split(',')[6])
        firedate = line.split(',')[7].strip(' 0:00:00')
        firedate = str(datetime.strptime(firedate, '%Y/%m/%d').strftime('%Y%m%d'))
        # if lat>32 and lat<42 and long_>-124 and long_<-114:
        if lat > 32 and lat < 34 and long_ > -118 and long_ < -114:
            wildfire_list.append((lat, long_, firedate))
    return wildfire_list


files_needed = []


def search(root):
    items = os.listdir(root)
    for item in items:
        path = os.path.join(root, item)
        if os.path.isdir(path):
            search(path)
        elif path.split('.')[-1] == 'asc':
            global files_needed
            files_needed.append(path)


def get_dicts(path, number_of_files):
    search(path)
    files_needed.sort(key=lambda x: x.split('_')[-2])
    filedicts = {}
    counter = 0
    for i, inputfile in enumerate(files_needed):
        if counter < number_of_files:
            extractor = ASC2XYZ(files_needed[i])
            filedicts.update(extractor.extract())
            counter += 1
    return filedicts


def get_feature_dicts(feature_filepaths, number_of_files):
    feature_dicts = []
    for feature in feature_filepaths:
        global files_needed
        files_needed = []
        feature_dict = get_dicts(feature, number_of_files)
        feature_dicts.append(feature_dict)
    files_needed = []
    return feature_dicts


def get_wildfire_looklike_features(feature_dicts, wildfire_records):
    labels_dict = dict()
    feature_values = []
    for wildfire in wildfire_records:
        fire_date = wildfire[2]
        base_lat_long_value_dict = feature_dicts[0].get(fire_date)
        if base_lat_long_value_dict is not None:
            for key, value in base_lat_long_value_dict.items():
                feature_values.append(value)
                if key[0] > wildfire[0] - 0.1 and key[0] < wildfire[0] + 0.1 \
                        and key[1] > wildfire[1] - 0.1 and key[1] > wildfire[1] + 0.1:
                    for i, feature_dict in enumerate(feature_dicts):
                        if i == 0:
                            continue
                        cur_feature_lat_long_dict = feature_dicts[i].get(fire_date)
                        if cur_feature_lat_long_dict is not None:
                            if cur_feature_lat_long_dict.get(key) is not None:
                                feature_values.append(cur_feature_lat_long_dict.get(key))
                if len(feature_values) == len(feature_dicts):
                    labels_dict[tuple(feature_values)] = 1
                feature_values = []
    return labels_dict


def prepare_data(feature_dicts, labels_dict):
    X = []
    y = []
    points = []
    base_feature_dict = feature_dicts[0]
    feature_value_set = []

    for key, value in base_feature_dict.items():  # date: dict
        for key1, value1 in value.items():  # lat,long: value
            feature_value_set.append(value1)
            for i, feature_dict in enumerate(feature_dicts):
                if i == 0:
                    continue
                cur_feature_lat_long_dict = feature_dicts[i].get(key)
                if cur_feature_lat_long_dict is not None:
                    if cur_feature_lat_long_dict.get(key1) is not None:
                        feature_value_set.append(cur_feature_lat_long_dict.get(key1))
            if len(feature_value_set) == len(feature_dicts):
                points.append(key1)
                X.append(feature_value_set)
                if labels_dict.get(tuple(feature_value_set)) is not None:
                    y.append(1)
                else:
                    y.append(0)
            feature_value_set = []
    X = np.array(X)
    y = np.array(y)
    points = np.array(points)
    return points, X, y


def prepare_testing_data(feature_dicts):
    X = []
    points = []
    base_feature_dict = feature_dicts[0]
    feature_value_set = []

    for key, value in base_feature_dict.items():  # date: dict
        for key1, value1 in value.items():  # lat,long: value
            feature_value_set.append(value1)
            for i, feature_dict in enumerate(feature_dicts):
                if i == 0:
                    continue
                cur_feature_lat_long_dict = feature_dicts[i].get(key)
                if cur_feature_lat_long_dict is not None:
                    if cur_feature_lat_long_dict.get(key1) is not None:
                        feature_value_set.append(cur_feature_lat_long_dict.get(key1))
            if len(feature_value_set) == len(feature_dicts):
                points.append(key1)
                X.append(feature_value_set)
            feature_value_set = []
    X = np.array(X)
    points = np.array(points)
    return points, X


def save_model(clf, path):
    with open(path, 'wb') as f:
        pickle.dump(clf, f)


def test_model(testing_points, test_data, path_to_model, path_to_save_results):
    true_count = 0
    with open(path_to_model, 'rb') as f:
        clf = pickle.load(f)
        result_file = open(path_to_save_results, 'w')
        result_file.write(
            '     latitude          longitude       temp   ppt     false-prob         true-prob     predict\n')
        for i, point in enumerate(testing_points):
            cur_data = test_data[i].reshape(1, -1)
            predict = clf.predict_proba(cur_data)
            if len(predict[0]) == 1:
                predict = [[1, 0]]
            result_file.write(
                str(testing_points[i][0]) + ' ' + str(testing_points[i][1]) + ' ' + str(cur_data[0][0]) + ' '
                + str(cur_data[0][1]) + ' ' + str(predict[0][0]) + ' ' + str(predict[0][1]) + ' '
                + ('true' if predict[0][1] > predict[0][0] else 'false') + '\n')
            if predict[0][1] > predict[0][0]:
                true_count += 1
        result_file.close()

    print('testing predicted as true: ', true_count)


def validate_model(testing_points, test_data, labels, path_to_model, path_to_save_results):
    true_count = 0
    prediction = []
    with open(path_to_model, 'rb') as f:
        clf = pickle.load(f)
        result_file = open(path_to_save_results, 'w')
        result_file.write(
            '     latitude          longitude       temp   ppt     false-prob        true-prob     predict actual\n')
        for i, point in enumerate(testing_points):
            cur_data = test_data[i].reshape(1, -1)
            predict = clf.predict_proba(cur_data)
            if len(predict[0]) == 1:
                predict = [[1, 0]]
            result_file.write(
                str(testing_points[i][0]) + ' ' + str(testing_points[i][1]) + ' ' + str(cur_data[0][0]) + ' '
                + str(cur_data[0][1]) + ' ' + str(predict[0][0]) + ' ' + str(predict[0][1]) + ' ' + (
                    'true' if predict[0][1] > predict[0][0] else 'false')
                + ' ' + ('true' if labels[i] == 1 else 'false') + '\n')
            if predict[0][1] > predict[0][0]:
                prediction.append(1)
                true_count += 1
            else:
                prediction.append(0)
        result_file.close()

    print('validation predicted as true: ', true_count)
    accuracy = sum(labels == prediction) / len(labels)
    return accuracy


def training(feature_filepaths, number_of_files, wildfire_info_file, path_to_save_model):
    wildfire_records = export_wildfile_info(wildfire_info_file)
    feature_dicts = get_feature_dicts(feature_filepaths, number_of_files)
    labels_dict = get_wildfire_looklike_features(feature_dicts, wildfire_records)
    training_points, X, y = prepare_data(feature_dicts, labels_dict)
    print('training data size: ', len(X))
    print('training data labeled as true: ', len(X[(y == 1)]))
    clf.fit(X, y)
    if clf == RandomForestClassifier:
        print('feature importance: ', clf.feature_importances_)
    save_model(clf, path_to_save_model)


def validation(feature_filepaths, number_of_files, wildfire_info_file, path_to_model, path_to_results):
    wildfire_records = export_wildfile_info(wildfire_info_file)
    feature_dicts = get_feature_dicts(feature_filepaths, number_of_files)
    labels_dict = get_wildfire_looklike_features(feature_dicts, wildfire_records)
    validation_points, X, y = prepare_data(feature_dicts, labels_dict)
    print('validation data size: ', len(X))
    print('validation data labeled as true: ', len(X[(y == 1)]))
    accuracy = validate_model(validation_points, X, y, path_to_model, path_to_results)
    print('validation accuracy: ', accuracy)


def testing(feature_filepaths, number_of_files, path_to_model, path_to_results):
    feature_dicts = get_feature_dicts(feature_filepaths, number_of_files)
    testing_points, X = prepare_testing_data(feature_dicts)
    print('testing data size: ', len(X))
    test_model(testing_points, X, path_to_model, path_to_results)


if __name__ == '__main__':
    training_filepaths = ['/Users/gutingxuan/Desktop/2018tmax', '/Users/gutingxuan/Desktop/2018ppt']
    training_wildfire_info_file = '/Users/gutingxuan/Desktop/Wildfires/satellite_classification/2018_Export_Output.txt'

    validation_filepaths = ['/Users/gutingxuan/Desktop/2018tmax', '/Users/gutingxuan/Desktop/2018ppt']
    validation_wildfire_info_file = '/Users/gutingxuan/Desktop/Wildfires/satellite_classification/2018_Export_Output.txt'
    path_to_validation_results = '/Users/gutingxuan/Desktop/Wildfires/satellite_classification/validation_results.txt'

    testing_filepaths = ['/Users/gutingxuan/Desktop/2018tmax', '/Users/gutingxuan/Desktop/2018ppt']
    path_to_testing_results = '/Users/gutingxuan/Desktop/Wildfires/satellite_classification/testing_results.txt'

    path_to_model = '/Users/gutingxuan/Desktop/Wildfires/satellite_classification/clf.pickle'

    number_of_files = 2
    # clf = RandomForestClassifier(n_estimators=100, max_depth=2, random_state=0)
    # clf = LogisticRegression(random_state=0, solver='lbfgs', multi_class='multinomial')
    # clf = MLPClassifier()
    clf = SVC(probability=True)

    training(training_filepaths, number_of_files, training_wildfire_info_file, path_to_model)
    print('\n')
    validation(validation_filepaths, number_of_files, validation_wildfire_info_file, path_to_model,
               path_to_validation_results)
    print('\n')
    testing(testing_filepaths, number_of_files, path_to_model, path_to_testing_results)
