import dataclasses
import os
import tempfile
from typing import List

from buildflow.dependencies import dependency, Scope
from imageai.Classification import ImageClassification


@dataclasses.dataclass
class Classification:
    classification: str
    confidence: float


@dependency(scope=Scope.REPLICA)
class Model:
    def __init__(self) -> None:
        self._execution_path = os.path.dirname(os.path.realpath(__file__))
        self._prediction = ImageClassification()
        self._prediction.setModelTypeAsMobileNetV2()
        self._prediction.setModelPath("mobilenet_v2-b0353104.pth")
        self._prediction.loadModel()

    def predict(self, file_bytes: bytes, result_count: int = 5) -> List[Classification]:
        with tempfile.NamedTemporaryFile() as tf:
            tf.write(file_bytes)
            predictions, probabilities = self._prediction.classifyImage(
                tf.name, result_count=result_count
            )

            classifications = []
            for predicition, probability in zip(predictions, probabilities):
                classifications.append(Classification(predicition, probability))
            return classifications
