from abc import ABC, abstractmethod
from typing import Union, Dict, List, Tuple


class ClassifierBase(ABC):
    def __init__(self):
        self.model = None

    @abstractmethod
    def set_model(self, model: Union[object, str]) -> None:
        """set the model to be used for prediction. it could be a python object or a path to the object"""
        pass

    @abstractmethod
    def predict(self, *args, **kwargs) -> Union[Dict, List, Tuple]:
        """predict the given argument with the model"""
        pass

    def train(self):
        """to be override only if needed"""
        pass
