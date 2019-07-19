import os
import torch
from torchvision import transforms
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

    def set_model(self, model: str = None):
        '''load trained model'''
        self.model = CNN(ImageClassifier.N_CHANNELS, ImageClassifier.N_CLASSES)
        if model:
            self.model.load_state_dict(torch.load(model))
        else:
            self.model.load_state_dict(torch.load(paths.IMAGE_CLASSIFIER_MODEL_PATH))

    def predict(self, url: str):
        '''predict classification result of the image from url'''
        print("url: " + url)
        # download image from url
        image_path = self.download_image(url)
        # transform image
        image = self.transform_image(image_path)
        if image is None:
            return [1, -1]
        # predict classification result
        outputs = self.model(image)
        os.remove(image_path)
        # outputs.data is a two-dimentional tensor, [0] means the first dimention, then convert tensor to list
        return outputs.data[0].tolist()

    def download_image(self, url):
        '''download image from url'''
        if not os.path.exists(paths.TWEET_IMAGES_DIR):
            os.makedirs(paths.TWEET_IMAGES_DIR)
        download_path = paths.TWEET_IMAGES_DIR + "/current.jpg"
        os.system(f"curl {url} --output {download_path}")
        return download_path

    def transform_image(self, image_path):
        '''image transformation to specific size'''
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
