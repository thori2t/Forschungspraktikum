from types import SimpleNamespace
import os
os.environ["HIP_VISIBLE_DEVICES"] = "0"
import torch
import numpy as np
import logging
import cv2
from timm.utils import setup_default_logging
from mivolo.structures import PersonAndFaceResult
from mivolo.model.mi_volo import MiVOLO
from mivolo.model.yolo_detector import Detector

#_logger = logging.getLogger("inference")
_logger = logging.getLogger("INFO")

class myMiVOLO(MiVOLO):
    def myPredict(self, image: np.ndarray, detected_bboxes: PersonAndFaceResult):
        if (
            (detected_bboxes.n_objects == 0)
            or (not self.meta.use_persons and detected_bboxes.n_faces == 0)
            or (self.meta.disable_faces and detected_bboxes.n_persons == 0)
        ):
            # nothing to process
            return 0, 0, 0

        faces_input, person_input, faces_inds, bodies_inds = self.prepare_crops(image, detected_bboxes)

        if faces_input is None and person_input is None:
            # nothing to process
            return 0, 0, 0

        if self.meta.with_persons_model:
            model_input = torch.cat((faces_input, person_input), dim=1)
        else:
            model_input = faces_input
        output = self.inference(model_input)
        ages, males, females = self.getAgeAndGender(output, faces_inds, bodies_inds)
        if (ages == None):
            ages = 0
        if (males == None):
            males = 0
        if (females == None):
            females = 0
        return ages, males, females

    def getAgeAndGender(self, output, faces_inds, bodies_inds):
        if self.meta.only_age:
            age_output = output
            gender_probs, gender_indx = None, None
        else:
            age_output = output[:, 2]
            gender_output = output[:, :2].softmax(-1)
            gender_probs, gender_indx = gender_output.topk(1)

        assert output.shape[0] == len(faces_inds) == len(bodies_inds)

        # [list of ages, [num of males, num of females]]
        totalAge = 0
        numOfMales = 0
        numOfFemales = 0

        # per face
        for index in range(output.shape[0]):
            # get_age
            age = age_output[index].item()
            age = age * (self.meta.max_age - self.meta.min_age) + self.meta.avg_age
            age = round(age, 2)

            _logger.info(f"\tage: {age}")
            totalAge += age

            if gender_probs is not None:
                gender = "male" if gender_indx[index].item() == 0 else "female"
                gender_score = gender_probs[index].item()

                _logger.info(f"\tgender: {gender} [{int(gender_score * 100)}%]")
                if(gender == "male"):
                    numOfMales += 1
                else:
                    numOfFemales += 1
        return totalAge, numOfMales, numOfFemales

# verkleinerter miVolo-Predictor
class myPredictor:
    def __init__(self, config, verbose: bool = False):
        self.detector = Detector(config.detector_weights, config.device, verbose=verbose)
        self.age_gender_model = myMiVOLO(
            config.checkpoint,
            config.device,
            half=True,
            use_persons=config.with_persons,
            disable_faces=config.disable_faces,
            verbose=verbose,
        )
        self.draw = config.draw

    def myRecognize(self, image: np.ndarray):
        detected_objects: PersonAndFaceResult = self.detector.predict(image)
        ages, males, females = self.age_gender_model.myPredict(image, detected_objects)
        if (ages == None):
            ages = 0
        if (males == None):
            males = 0
        if (females == None):
            females = 0
        return ages, males, females

def main():
    setup_default_logging()
    input="/run/media/thori2t/HDD_LUL/Forschungspraktikum/Images/"
    output="output/"
    config = SimpleNamespace(
        detector_weights="models/yolov8x_person_face.pt",
        checkpoint="models/model_imdb_cross_person_4.22_99.46.pth.tar",
        with_persons=True,
        disable_faces=False,
        draw=True, # hier false machen, damit keine Bilder für den Output Ordner erstellt werden
        device="cuda",
    )

    if torch.cuda.is_available():
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.benchmark = True
    os.makedirs(output, exist_ok=True)

    predictor = myPredictor(config, verbose=True)

    #test .paris
    #computeTopLevelDomain(input + "paris/", predictor)

    # .de
    germanInput = input + "de/"
    computeTopLevelDomain(germanInput, predictor)
    # .fr
    frenchInput = input +"fr/"
    computeTopLevelDomain(frenchInput, predictor)

def computeTopLevelDomain(path, predictor):
    totalAge = 0
    numMale = 0
    numFemale = 0
    _logger.info("topLevelDomainFolder: " + path)
    for topLevelDomainFolder, secondLevelFolders, files in os.walk(path):
        for secondLevelFolder in secondLevelFolders:
            _logger.info("secondLevelFolder: " + secondLevelFolder)
            ages, male, female = computeSecondLevelDomain(os.path.join(topLevelDomainFolder, secondLevelFolder), predictor)
            totalAge += ages
            numMale += male
            numFemale += female
            _logger.info("TopLeveldomain    " + topLevelDomainFolder)
            _logger.info("totalAge  " + str(totalAge))
            _logger.info("numMale   " + str(numMale))
            _logger.info("numFemale " + str(numFemale))
            _logger.info("----------------------------------------------ä----")
    _logger.info("topLevelDomainFolder + txt : " + path + "/results.txt" )
    writeResultsFile(path + "/results.txt", totalAge, numMale, numFemale)

def computeSecondLevelDomain(path, predictor):
    totalAge = 0
    numMale = 0
    numFemale = 0
    for secondLevelDomainFolder, innerSubFolders, images in os.walk(path):
        for img_p in images:
            if(".txt" in img_p):
                continue

            _logger.info("imagePath: " + img_p)
            img = cv2.imread(os.path.join(secondLevelDomainFolder, img_p))
            ages, male, female = predictor.myRecognize(img)
            totalAge += ages
            numMale += male
            numFemale += female
            _logger.info("domain    " + secondLevelDomainFolder)
            _logger.info("totalAge  " + str(totalAge))
            _logger.info("numMale   " + str(numMale))
            _logger.info("numFemale " + str(numFemale))
            _logger.info("----------------------------------------------ä----")

    writeResultsFile(secondLevelDomainFolder + "/results.txt", totalAge, numMale, numFemale)
    return totalAge, numMale, numFemale

def writeResultsFile(path, totalAge, numMale, numFemale):
    with open(path, "w") as f:
        f.write("\n--------------------------------")
        f.write("\ntotalAge: " + str(totalAge))
        f.write("\nnumPeople: " + str(numMale + numFemale))
        if(numMale + numFemale > 0):
            f.write("\naverage Age: " + str(totalAge / (numMale + numFemale)))
        f.write("\nnumMale: " + str(numMale))
        f.write("\nnumFemale: " + str(numFemale))

if __name__ == "__main__":
    main()
