import os
import wget
from urllib.error import HTTPError
import torch
import torchvision
from torch.autograd import Variable
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import torch.utils.data
import torchvision.models as models
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from PIL import Image

import rootpath

rootpath.append()
from backend.classifiers.classifierbase import ClassifierBase
from backend.models.cnn_module import CNN
import paths


class ImageClassifier(ClassifierBase):
    VGG_MODEL = "vgg"
    RESNET_MODEL = "resnet"

    N_CHANNELS = 3  # number of input channels (for VGG)
    N_CLASSES = 2  # number of classes of the classification problem (for VGG)
    DROPSIZE = 512  # drop size of the image transformation (for VGG)

    # parameters use for train process
    RESNET_MODEL_TYPE = torchvision.models.resnet.ResNet
    DATALOADER_TYPE = torch.utils.data.dataloader.DataLoader
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
        self.model_type = model_type

    def set_model(self, model: str = None):
        """load trained model"""

        if self.model_type == ImageClassifier.VGG_MODEL:
            self.model = CNN(ImageClassifier.N_CHANNELS, ImageClassifier.N_CLASSES)
            if model:
                self.model.load_state_dict(torch.load(model))
            else:
                self.model.load_state_dict(torch.load(paths.IMAGE_CLASSIFIER_VGG_PATH, map_location='cpu'))

        elif self.model_type == ImageClassifier.RESNET_MODEL:
            self.model = models.resnet50(pretrained=True, progress=True)
            if model:
                self.model.load_state_dict(torch.load(model))
            else:
                self.model.load_state_dict(torch.load(paths.IMAGE_CLASSIFIER_RESNET_PATH, map_location='cpu'))

    def predict(self, url: str) -> tuple:
        """predict classification result of the image from url"""

        print("url: " + url)
        # download image from url
        image_path = self.download_image(url)

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
        percentages = F.softmax(outputs, dim=1)

        # convert the percentage result from tensor type to list type, then return tuple
        if self.model_type == ImageClassifier.VGG_MODEL:
            return tuple(percentages.tolist()[0])
        elif self.model_type == ImageClassifier.RESNET_MODEL:
            return tuple(self.prettify(torch.topk(percentages, 2)))

    def train(self, train_path: str, val_path: str, num_epochs: int = EPOCHS) -> RESNET_MODEL_TYPE:
        """train model"""
        train_loader = ImageClassifier.load_dataloader(train_path, ImageClassifier.TRAIN_MODE)
        model = models.resnet50(pretrained=True, progress=True)
        loss_fn = nn.CrossEntropyLoss()
        optimizer = optim.RMSprop(model.parameters(), lr=ImageClassifier.LEARNING_RATE)

        for epoch in range(num_epochs):
            print('Starting epoch %d / %d' % (epoch + 1, num_epochs))
            model.train()
            for t, (x, y) in enumerate(train_loader):
                x_var = Variable(x)
                y_var = Variable(y.long())

                scores = model(x_var)
                loss = loss_fn(scores, y_var)
                print('t = %d, loss = %.4f' % (t + 1, loss.item()))
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
        return model

    @staticmethod
    def load_dataloader(dataset_path: str, process_mode: int) -> DATALOADER_TYPE:
        """pre-process dataset as dataloader"""
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
        """use test data to print out accuracy"""
        loader = self.load_dataloader(val_path, ImageClassifier.VAL_MODE)
        num_correct = 0
        num_samples = 0
        model.eval()  # Put the model in test mode (the opposite of model.train(), essentially)
        for x, y in loader:
            x_var = Variable(x, volatile=True)

            scores = model(x_var)
            _, preds = scores.data.cpu().max(1)
            num_correct += (preds == y).sum()
            num_samples += preds.size(0)
        acc = float(num_correct) / num_samples
        print('Got %d / %d correct (%.2f)' % (num_correct, num_samples, 100 * acc))

    def save_model(self, model: RESNET_MODEL_TYPE, modelname: str):
        """save the model locally"""
        torch.save(model.state_dict(), paths.MODELS_SAVE_PATH + modelname)

    def download_image(self, url: str) -> str:
        """download image from url"""
        if not os.path.exists(paths.TWEET_IMAGES_DIR):
            os.makedirs(paths.TWEET_IMAGES_DIR)
        download_path = paths.TWEET_IMAGES_DIR + "/current.jpg"
        try:
            wget.download(url=url, out=download_path)
        except HTTPError:
            print("HTTP Error 404: Website url not found.")
            return None
        except Exception as err:
            print(f"unexpected err {err}")
            return None
        return download_path

    def vgg_transform_image(self, image_path: str):
        """under VGG model, image transformation to specific size"""
        if image_path is None:
            return None
        trans = transforms.Compose(
            [
                transforms.CenterCrop(ImageClassifier.DROPSIZE),
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
            transformed_img = trans(img)
            transformed_img = transformed_img.view(1, ImageClassifier.RGB_CHANNELS, ImageClassifier.DROPSIZE,
                                                   ImageClassifier.DROPSIZE)
        except RuntimeError as err:
            print("RuntimeError: Tensor size mismatches with the model." + f" Detail: {err}")
            return None
        except Exception as err:
            print(f"unexpected err {err}")
            return None
        return transformed_img

    def resnet_transform_image(self, image_path: str):
        """under RESNET model, image transformation to specific size"""
        imsize = ImageClassifier.RESIZE_VALUE
        loader = transforms.Compose([transforms.Resize(imsize), transforms.ToTensor()])
        try:
            image = Image.open(image_path)
            image = loader(image).float()
            image = Variable(image, requires_grad=True)
            image = image.unsqueeze(0)
            # check if channel is 3
            if image.shape[1] != ImageClassifier.RGB_CHANNELS:
                return None
        except RuntimeError as err:
            print("RuntimeError: Tensor size mismatches with the model." + f" Detail: {err}")
            return None
        except Exception as err:
            print(f"unexpected err {err}")
            return None
        return image.cpu()

    def prettify(self, tensor_topk) -> list:
        """transfer tensor object into list of confidence level"""
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

    # train model, parameters are path of train dataset and validation dataset
    train_path = "/Users/wangyutong/PycharmProjects/wildfire_prediction/Data/train"
    val_path = "/Users/wangyutong/PycharmProjects/wildfire_prediction/Data/val"
    model = image_classifier.train(train_path, val_path)

    # save the model locally
    image_classifier.save_model(model, modelname="ResNet50.ckpt")

    # check and print accuracy
    image_classifier.check_accuracy(model, val_path)
