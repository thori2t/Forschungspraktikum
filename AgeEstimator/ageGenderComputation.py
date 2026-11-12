from types import SimpleNamespace
import logging
import os
import numpy as np
import cv2
import torch
from timm.utils import setup_default_logging
from mivolo.structures import AGE_GENDER_TYPE, PersonAndFaceResult
from mivolo.model.mi_volo import MiVOLO
from mivolo.model.yolo_detector import Detector
from typing import Optional, Tuple

#_logger = logging.getLogger("inference")

# verkleinerter miVolo-Predictor
class Predictor:
    def __init__(self, config, verbose: bool = False):
        self.detector = Detector(config.detector_weights, config.device, verbose=verbose)
        self.age_gender_model = MiVOLO(
            config.checkpoint,
            config.device,
            half=True,
            use_persons=config.with_persons,
            disable_faces=config.disable_faces,
            verbose=verbose,
        )
        self.draw = config.draw

    def recognize(self, image: np.ndarray) -> Tuple[PersonAndFaceResult, Optional[np.ndarray]]:
        detected_objects: PersonAndFaceResult = self.detector.predict(image)
        self.age_gender_model.predict(image, detected_objects)

        out_im = None
        if self.draw:
            # plot results on image
            out_im = detected_objects.plot()
            return detected_objects, out_im


def main():
    setup_default_logging()
    input="/home/thori2t/Documents/Uni/5. Semester/Forschungspraktikum/WebCrawler/Forschungspraktikum/images/"
    output="output/"
    config = SimpleNamespace(
        detector_weights="yolov8x_person_face.pt",
        checkpoint="model_imdb_cross_person_4.22_99.46.pth.tar",
        with_persons=True,
        disable_faces=False,
        draw=True, # hier false machen, damit keine Bilder für den Output Ordner erstellt werden
        device="cpu",
    )

    if torch.cuda.is_available():
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.benchmark = True
    os.makedirs(output, exist_ok=True)

    predictor = Predictor(config, verbose=True)

    # .de
    germanInput = input + "de/"
    computeTopLevelDomain(germanInput, predictor)
    # .fr
    frenchInput = input +"fr/"
    computeTopLevelDomain(frenchInput, predictor)

def computeTopLevelDomain(path, predictor):
    for topLevelDomainFolder, secondLevelFolders, files in os.walk(path):
        for secondLevelFolder in secondLevelFolders:
            print(secondLevelFolder)
            computeSecondLevelDomain(os.path.join(topLevelDomainFolder, secondLevelFolder), predictor)

def computeSecondLevelDomain(path, predictor):
    totalAge = 0
    numMale = 0
    numFemale = 0
    for secondLevelDomainFolder, innerSubFolders, images in os.walk(path):
        for img_p in images:
            print()
            img = cv2.imread(os.path.join(secondLevelDomainFolder, img_p))
            detected_objects, out_im = predictor.recognize(img)
            #print("detectedObjects:")
            #print(detected_objects)
            #age = detected_objects.age_output[0].item()

if __name__ == "__main__":
    main()
