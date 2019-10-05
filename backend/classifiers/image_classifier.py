"""
@author: Yutong Wang, (Hugo) Qiaonan Huang
"""
import logging
import os
import traceback
from typing import Optional, Any
from urllib.error import HTTPError

import rootpath
import torch
import torch.nn as nn
import torch.nn.functional as functional
import torch.optim as optim
import torch.utils.data
import torchvision
import torchvision.datasets as datasets
import torchvision.models as models
import torchvision.transforms as transforms
import wget
from PIL import Image
from torch.autograd import Variable

rootpath.append()
from backend.classifiers.classifierbase import ClassifierBase
from backend.models.cnn_module import CNN
import paths

logger = logging.getLogger('TaskManager')


class ImageClassifier(ClassifierBase):
    """
    Image classifier can either use model to predict or train the model.
    """
    VGG_MODEL = "vgg"
    RESNET_MODEL = "resnet"

    N_CHANNELS = 3  # number of input channels (for VGG)
    N_CLASSES = 2  # number of classes of the classification problem (for VGG)
    DROP_SIZE = 512  # drop size of the image transformation (for VGG)

    # parameters use for train process
    RESNET_MODEL_TYPE = torchvision.models.resnet.ResNet
    DATA_LOADER_TYPE = torch.utils.data.dataloader.DataLoader
    TRAIN_MODE = 0
    VAL_MODE = 1
    LEARNING_RATE = 1e-4
    NORMALIZE_PARAM_MEAN_0 = 0.485
    NORMALIZE_PARAM_MEAN_1 = 0.456
    NORMALIZE_PARAM_MEAN_2 = 0.406
    NORMALIZE_PARAM_STD_0 = 0.229
    NORMALIZE_PARAM_STD_1 = 0.224
    NORMALIZE_PARAM_STD_2 = 0.225
    CROP_VALUE = 224
    RESIZE_VALUE = 256
    EPOCHS = 1
    BATCH_SIZE = 32
    NUM_WORKERS = 4
    RGB_CHANNELS = 3

    def __init__(self, model_type: str):
        """
        Init function of image classifier class.
        :param model_type: different model will be used according to model type.
        """
        super().__init__()
        self.model_type = model_type
        if torch.cuda.is_available():
            self.dtype = torch.cuda.FloatTensor
        else:
            self.dtype = torch.float

    def set_model(self, model: str = None):
        """
        Loads trained model accrording to model_type of the class.
        :param model: the path of trained model. If not none, then load the specific model.
        """

        if self.model_type == ImageClassifier.VGG_MODEL:
            self.model = CNN(ImageClassifier.N_CHANNELS, ImageClassifier.N_CLASSES)
            if model:
                self.model.load_state_dict(torch.load(model))
            else:
                self.model.load_state_dict(torch.load(paths.IMAGE_CLASSIFIER_VGG_PATH, map_location='cpu'))

        elif self.model_type == ImageClassifier.RESNET_MODEL:
            self.model = models.resnet50(pretrained=True, progress=True).type(self.dtype)
            if model:
                self.model.load_state_dict(torch.load(model)).type(self.dtype)
            else:
                self.model.load_state_dict(torch.load(paths.IMAGE_CLASSIFIER_RESNET_PATH, map_location='cpu')).type(
                    self.dtype)

    def predict(self, url: str) -> tuple:
        """
        Predicts classification result of the image from url.
        :param url: the url link for an image.
        :return: prediction result for this image. Result type is a tuple containing probability of being a wildfire or not wildfire. Two probabilities add up to 1.
        """

        logger.info("predicting url: " + url)
        # download image from url
        image_path = self.download_image(url)

        # assign image
        image = None

        # transform image
        if self.model_type == ImageClassifier.VGG_MODEL:
            image = self.vgg_transform_image(image_path)
        elif self.model_type == ImageClassifier.RESNET_MODEL:
            image = self.resnet_transform_image(image_path)
            # set resnet model to evalution mode
            self.model.eval()
        # if fail to open image, then image is None type, defaultly output the image as "not wildfire"
        if image is None:
            if image_path is not None:
                # delete the downloaded image
                os.remove(image_path)
            return 1, 0
        # predict classification result
        outputs = self.model(image)

        # delete the downloaded image
        os.remove(image_path)

        # use softmax layer to get percentage prediction result
        percentages = functional.softmax(outputs, dim=1)

        # convert the percentage result from tensor type to list type, then return tuple
        if self.model_type == ImageClassifier.VGG_MODEL:
            return tuple(percentages.tolist()[0])
        elif self.model_type == ImageClassifier.RESNET_MODEL:
            return tuple(self.prettify(torch.topk(percentages, 2)))

    def train(self, train_path: str, num_epochs: int = EPOCHS) -> RESNET_MODEL_TYPE:
        """
        Trains a CNN model using ResNet50.

        Basic structures:
            Training Data: Preprocessed data in a format of 32(default) batch size loader
            Loss function: Cross Entropy Loss
            Optimizer: rmsprop

        :param train_path: Path of training data
        :param num_epochs: Number of epochs used to train data.
        :return: model trained with training data
        """
        # 1. build data loader for training dataset from the path train_path.
        train_loader = ImageClassifier.load_dataloader(train_path, ImageClassifier.TRAIN_MODE)

        # 2. set up the resnet model from the library
        model = models.resnet50(pretrained=True, progress=True)

        # 3. set up the loss object and optimizer
        loss_fn = nn.CrossEntropyLoss()
        optimizer = optim.RMSprop(model.parameters(), lr=ImageClassifier.LEARNING_RATE)

        # 4. train on several epoch based on the value of EPOCH
        for epoch in range(num_epochs):
            logger.info('Starting epoch %d / %d' % (epoch + 1, num_epochs))
            model.train()
            for t, (x, y) in enumerate(train_loader):
                x_var = Variable(x.type(self.dtype))
                y_var = Variable(y.type(self.dtype).long())

                scores = model(x_var)
                loss = loss_fn(scores, y_var)
                logger.info('t = %d, loss = %.4f' % (t + 1, loss.item()))
                optimizer.zero_grad()
                # backward propagation
                loss.backward()
                # optimize parameters
                optimizer.step()
        return model

    @staticmethod
    def load_dataloader(dataset_path: str, process_mode: int) -> DATA_LOADER_TYPE:
        """
        Preprocesses training or testing data into dataloader.

        Process including:
            1. Normalization
            2. RandomResizedCrop
            3. RandomHorizontalFlip

        :param dataset_path: Path of training or testing data.
        :param process_mode: Used to distinguished training or testing mode.
        :return: dataloder which can be used to do training or validating.
        """
        normalize = transforms.Normalize(mean=[ImageClassifier.NORMALIZE_PARAM_MEAN_0,
                                               ImageClassifier.NORMALIZE_PARAM_MEAN_1,
                                               ImageClassifier.NORMALIZE_PARAM_MEAN_2],
                                         std=[ImageClassifier.NORMALIZE_PARAM_STD_0,
                                              ImageClassifier.NORMALIZE_PARAM_STD_1,
                                              ImageClassifier.NORMALIZE_PARAM_STD_2])

        if process_mode == ImageClassifier.TRAIN_MODE:
            dataloader = torch.utils.data.DataLoader(
                datasets.ImageFolder(dataset_path, transforms.Compose([
                    transforms.RandomResizedCrop(ImageClassifier.CROP_VALUE),
                    transforms.RandomHorizontalFlip(),
                    transforms.ToTensor(),
                    normalize,
                ])),
                batch_size=ImageClassifier.BATCH_SIZE, shuffle=True,
                num_workers=ImageClassifier.NUM_WORKERS, pin_memory=True)

        elif process_mode == ImageClassifier.VAL_MODE:
            dataloader = torch.utils.data.DataLoader(
                datasets.ImageFolder(dataset_path, transforms.Compose([
                    transforms.Resize(ImageClassifier.RESIZE_VALUE),
                    transforms.CenterCrop(ImageClassifier.CROP_VALUE),
                    transforms.ToTensor(),
                    normalize,
                ])),
                batch_size=ImageClassifier.BATCH_SIZE, shuffle=False,
                num_workers=ImageClassifier.NUM_WORKERS, pin_memory=True)

        return dataloader

    def check_accuracy(self, model: RESNET_MODEL_TYPE, val_path: str):
        """
        Uses test data to print out accuracy

        :param model: Trained model used to check accuracy
        :param val_path: Path of testing data
        """
        loader = self.load_dataloader(val_path, ImageClassifier.VAL_MODE)
        num_correct = 0
        num_samples = 0
        model.eval()  # Put the model in test mode (the opposite of model.train(), essentially)
        for x, y in loader:
            x_var = Variable(x.type(self.dtype), volatile=True)

            scores = model(x_var)
            _, preds = scores.data.cpu().max(1)
            num_correct += (preds == y).sum()
            num_samples += preds.size(0)
        acc = float(num_correct) / num_samples
        logger.info('Got %d / %d correct (%.2f)' % (num_correct, num_samples, 100 * acc))

    @staticmethod
    def save_model(model: RESNET_MODEL_TYPE, modelname: str):
        """
        Saves the model locally.

        :param model: Trained model.
        :param modelname: Trained model name.
        """
        torch.save(model.state_dict(), paths.MODELS_SAVE_PATH + modelname)

    @staticmethod
    def download_image(url: str) -> Optional[str]:
        """
        Downloads image from url.
        :param url: url link of the image.
        :return: download path for the image.
        """
        if not os.path.exists(paths.TWEET_IMAGES_DIR):
            os.makedirs(paths.TWEET_IMAGES_DIR)
        download_path = paths.TWEET_IMAGES_DIR + "/current.jpg"
        try:
            wget.download(url=url, out=download_path)
            return download_path
        except HTTPError:
            logger.error("HTTP Error 404: Website url not found.")
        except Exception:
            logger.error("error: " + traceback.format_exc())

    @staticmethod
    def vgg_transform_image(image_path: str) -> Optional[Any]:
        """
        Transforms image to specific size under VGG model.
        :param image_path: path of image.
        :return: transformed image with specific size of tensor type.
        """
        if image_path is None:
            return None
        # specify a specific transformation for all the images
        trans = transforms.Compose(
            [
                transforms.CenterCrop(ImageClassifier.DROP_SIZE),
                transforms.ToTensor(),
                transforms.Normalize([ImageClassifier.NORMALIZE_PARAM_MEAN_0,
                                      ImageClassifier.NORMALIZE_PARAM_MEAN_1,
                                      ImageClassifier.NORMALIZE_PARAM_MEAN_2],
                                     [ImageClassifier.NORMALIZE_PARAM_STD_0,
                                      ImageClassifier.NORMALIZE_PARAM_STD_1,
                                      ImageClassifier.NORMALIZE_PARAM_STD_2])

            ])
        try:
            img = Image.open(image_path)
            # return the image with same size as other images
            return trans(img).view(1, ImageClassifier.RGB_CHANNELS, ImageClassifier.DROP_SIZE,
                                   ImageClassifier.DROP_SIZE)
        except RuntimeError as err:
            logger.error("RuntimeError: Tensor size mismatches with the model." + f" Detail: {err}")
        except Exception:
            logger.error("error: " + traceback.format_exc())

    @staticmethod
    def resnet_transform_image(image_path: str):
        """
        Transforms image to specific size under RESNET model.
        :param image_path: path of image.
        :return: transformed image with specific size of tensor type.
        """
        # specify a specific transformation for all the images
        trans = transforms.Compose([transforms.Resize(ImageClassifier.RESIZE_VALUE), transforms.ToTensor()])
        try:
            image = Variable(trans(Image.open(image_path)).float(), requires_grad=True).unsqueeze(0)
            # check if channel is 3
            if image.shape[1] != ImageClassifier.RGB_CHANNELS:
                return None
            return image.cpu()
        except RuntimeError as err:
            logger.error("RuntimeError: Tensor size mismatches with the model." + f" Detail: {err}")

        except Exception:
            logger.error("error: " + traceback.format_exc())

    @staticmethod
    def prettify(tensor_topk) -> list:
        """
        Transfers tensor object into list of confidence level. From tensor Object to a list, where index
        representing the class and the value of the index representing the probability.

        :param tensor_topk: Top 2 tensor object which contains the corresponding probability of each class.
        :return: A list of corresponding probability.
        """
        result = [0, 0]
        idx = [0, 0]
        prob = [0, 0]
        for i in range(tensor_topk.n_fields):
            idx[i] = tensor_topk.indices.data.cpu()[0][i].item()
            prob[i] = tensor_topk.values.data.cpu()[0][i].item()
        # change the larger index value to 1, and the smaller index value to 0,
        # so the prediction result has correct correspondence between classification class and prediction value
        if idx[0] < idx[1]:
            idx = [0, 1]
        else:
            idx = [1, 0]
        result[idx[0]] = prob[0]
        result[idx[1]] = prob[1]
        return result


if __name__ == '__main__':
    image_classifier = ImageClassifier(ImageClassifier.RESNET_MODEL)
    image_classifier.set_model()
    # test case
    prediction_result = image_classifier.predict('https://pbs.twimg.com/media/De1Oc7XU8AA5JcO.jpg')
    print(prediction_result)

    # train model, parameters are path of training dataset and validation dataset

    # Instructions on making image dataset:
    #   To create training dataset and validation dataset for tweet images, first make a directory named image_dataset
    #   in ROOTDIR/data/ ,within ROOTDIR/data/image_dataset, make 2 directories named train and val, then in both train
    #   and val, make 2 directories called "wildfire" and "not-wildfire", put images into them respectively.
    # Example(numbers below are for example, the more images the better):
    #   put 400 wildfire images into ROOTDIR/data/image_dataset/train/wildfire
    #   put 400 not wildfire images into ROOTDIR/data/image_dataset/train/not-wildfire
    #   put another 100 wildfire images into ROOTDIR/data/image_dataset/val/wildfire
    #   put another 100 not wildfire images into ROOTDIR/data/image_dataset/val/not-wildfire
    train_path = paths.IMAGE_TRAIN_PATH
    val_path = paths.IMAGE_VAL_PATH
    model = image_classifier.train(train_path)

    # save the model locally
    image_classifier.save_model(model, modelname="ResNet50.ckpt")

    # check and print accuracy
    image_classifier.check_accuracy(model, val_path)
