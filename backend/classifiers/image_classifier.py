import os
import torch
from torchvision import transforms
from torch.autograd import Variable
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import torch.utils.data
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

    def train(self, model, loss_fn, optimizer, train_path, num_epochs=5):
        train_loader = self.load_train(train_path)

        for epoch in range(num_epochs):
            print('Starting epoch %d / %d' % (epoch + 1, num_epochs))
            model.train()
            for t, (x, y) in enumerate(train_loader):
                x_var = Variable(x)
                y_var = Variable(y.long())

                scores = model(x_var)

                loss = loss_fn(scores, y_var)
                if (t + 1) % 100 == 0:
                    print('t = %d, loss = %.4f' % (t + 1, loss.item()))

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

    def load_train(self, traindir):
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


if __name__ == '__main__':
    image_classifier = ImageClassifier()
    image_classifier.set_model()
    # test case
    prediction_result = image_classifier.predict('https://pbs.twimg.com/media/CxT4tldUkAAN68b.jpg')
    print(prediction_result)