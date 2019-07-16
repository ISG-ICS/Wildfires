from typing import Union, Dict, List, Tuple, Optional

import rootpath

rootpath.append()
from backend.classifiers.classifierbase import ClassifierBase


class Event2MindClassifier(ClassifierBase):
    XREC= 0

    def set_model(self, model: Union[object, str]) -> None:
        pass

    def predict(self, text: str, target:Optional[int]= None) -> Union[Dict, List, Tuple]:
        pass

if __name__ == '__main__':
    event2mindClassifier = Event2MindClassifier()

    event2mindClassifier.set_model()
    event2mindClassifier.predict("hello", event2mindClassifier.XREC)