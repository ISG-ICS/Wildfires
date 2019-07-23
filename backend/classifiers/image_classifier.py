import os
import torch
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
    N_CHANNELS = 3  # number of input channels
    N_CLASSES = 2  # number of classes of the classification problem
    DROPSIZE = 512  # drop size of the image transformation
    VGG_MODEL = "vgg"
    RESNET_MODEL = "resnet"

    def __init__(self, model_type: str):
        self.model_type = model_type

    def set_model(self, model: str = None):
        '''load trained model'''

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

    def predict(self, url: str):
        '''predict classification result of the image from url'''

        print("url: " + url)
        # download image from url
        image_path = self.download_image(url)

        # transform image
        if self.model_type == ImageClassifier.VGG_MODEL:
            image = self.vgg_transform_image(image_path)
        elif self.model_type == ImageClassifier.RESNET_MODEL:
            image = self.resnet_transform_image(image_path)
        # if fail to open image, then image is None type, defaultly output the image as "not wildfire"
        if image is None:
            return [1, -1]

        # predict classification result
        outputs = self.model(image)

        # delete the downloaded image
        os.remove(image_path)

        # use softmax layer to get percentage prediction result
        percentages = F.softmax(outputs, dim=1)

        # convert the percentage result from tensor type to list type
        if self.model_type == ImageClassifier.VGG_MODEL:
            return percentages.tolist()[0]
        elif self.model_type == ImageClassifier.RESNET_MODEL:
            return self.prettify(torch.topk(percentages, 2))

    def train(self, train_path, val_path, num_epochs=1):
        """ 1. train model
            2. check accuracy
            3. save the model locally """
        train_loader = self.load_train(train_path)
        model = models.resnet50(pretrained=True, progress=True)
        loss_fn = nn.CrossEntropyLoss()
        optimizer = optim.RMSprop(model.parameters(), lr=1e-4)

        for epoch in range(num_epochs):
            print('Starting epoch %d / %d' % (epoch + 1, num_epochs))
            model.train()
            for t, (x, y) in enumerate(train_loader):
                x_var = Variable(x)
                y_var = Variable(y.long())

                scores = model(x_var)

                loss = loss_fn(scores, y_var)
                # if (t + 1) % 100 == 0:
                print('t = %d, loss = %.4f' % (t + 1, loss.item()))

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
        # save model into defalt path
        torch.save(model.state_dict(), paths.MODELS_SAVE_PATH + "ResNet50.ckpt")
        self.check_accuracy(model, val_path)

    def load_train(self, traindir):
        """ pre-process training data as dataloader """
        normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                         std=[0.229, 0.224, 0.225])

        train_loader = torch.utils.data.DataLoader(
            datasets.ImageFolder(traindir, transforms.Compose([
                transforms.RandomResizedCrop(224),
                transforms.RandomHorizontalFlip(),
                transforms.ToTensor(),
                normalize,
            ])),
            batch_size=32, shuffle=True,
            num_workers=4, pin_memory=True)
        return train_loader

    def load_val(self, val_path):
        """ pre-process testing data as dataloader """
        normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                         std=[0.229, 0.224, 0.225])

        val_loader = torch.utils.data.DataLoader(
            datasets.ImageFolder(val_path, transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                normalize,
            ])),
            batch_size=32, shuffle=False,
            num_workers=4, pin_memory=True)
        return val_loader

    def check_accuracy(self, model, val_path):
        """ use test data to print out accuracy """
        loader = self.load_val(val_path)
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
        return acc

    def download_image(self, url):
        '''download image from url'''
        if not os.path.exists(paths.TWEET_IMAGES_DIR):
            os.makedirs(paths.TWEET_IMAGES_DIR)
        download_path = paths.TWEET_IMAGES_DIR + "/current.jpg"
        os.system(f"curl {url} --output {download_path}")
        return download_path

    def vgg_transform_image(self, image_path):
        '''Using VGG model, image transformation to specific size'''
        trans = transforms.Compose(
            [
                transforms.CenterCrop(ImageClassifier.DROPSIZE),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])

            ])
        try:
            img = Image.open(image_path)
            transformed_img = trans(img)
            transformed_img = transformed_img.view(1, 3, ImageClassifier.DROPSIZE, ImageClassifier.DROPSIZE)
        except Exception as err:
            print("error", err)
            return None
        return transformed_img

    def resnet_transform_image(self, image_path):
        '''Using RESNET model, image transformation to specific size'''
        imsize = 256
        loader = transforms.Compose([transforms.Resize(imsize), transforms.ToTensor()])
        try:
            image = Image.open(image_path)
            image = loader(image).float()
            image = Variable(image, requires_grad=True)
            image = image.unsqueeze(0)
            # check if channel is 3
            if image.tolist()[1] != 3:
                return None
        except Exception as err:
            print("error", err)
            return None
        return image.cpu()

    def prettify(self, tensor_topk):
        """transfer tensor object into list of confidence level"""
        result = []
        for i in range(tensor_topk.n_fields):
            result.append(tensor_topk.values.data.cpu()[0][i].item())
        return result


if __name__ == '__main__':
    image_classifier = ImageClassifier("resnet")
    image_classifier.set_model()
    # test case
    prediction_result = image_classifier.predict('https://pbs.twimg.com/media/CxT4tldUkAAN68b.jpg')
    print(prediction_result)

    # training process(independent), parameters are path of train dataset and validation dataset
    image_classifier.train("/Users/wangyutong/PycharmProjects/wildfire_prediction/Data/train",
                           "/Users/wangyutong/PycharmProjects/wildfire_prediction/Data/val")
