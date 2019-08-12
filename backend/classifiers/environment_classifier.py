import torch
import torch.nn.functional as F
import rootpath

rootpath.append()

from backend.classifiers.classifierbase import ClassifierBase
from backend.models.env_cnn_module import CNN
import paths


class EnvironmentClassifier(ClassifierBase):
    ENV_IMG_ROW = 228
    ENV_IMG_COLUMN = 248

    def set_model(self, model: str = None):
        """load trained model"""
        self.model = CNN().double()
        if model:
            self.model.load_state_dict(torch.load(model))
        else:
            self.model.load_state_dict(torch.load(paths.ENV_CLASSIFIER_PATH))

    def predict(self, env_features) -> list:
        """predict the given argument with the model"""
        env_features = torch.unsqueeze(torch.tensor(env_features), dim=0)
        output = self.model(env_features)

        prediction_result = []
        for i in range(EnvironmentClassifier.ENV_IMG_ROW):
            prediction_result.append([])
            for j in range(EnvironmentClassifier.ENV_IMG_COLUMN):
                prediction = [output[0][0][i][j], output[0][1][i][j]]
                prediction_prob = F.softmax(torch.tensor(prediction), dim=0)
                prediction_result[i].append(prediction_prob[1].data.numpy().tolist())

        # size of prediction_result is ENV_IMG_ROW * ENV_IMG_COLUMN (228, 248)
        return prediction_result

