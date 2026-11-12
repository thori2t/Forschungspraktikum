from types import SimpleNamespace
import logging
import os
import cv2
import torch
from mivolo.data.data_reader import get_all_files
from mivolo.predictor import Predictor
from timm.utils import setup_default_logging

_logger = logging.getLogger("inference")


def main():
    setup_default_logging()

    args = SimpleNamespace(
        input="/home/thori2t/Documents/Uni/5. Semester/Forschungspraktikum/WebCrawler/Forschungspraktikum/images/de/www.tu-chemnitz.de/",
        output="output/",
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
    os.makedirs(args.output, exist_ok=True)

    predictor = Predictor(args, verbose=True)

    image_files = get_all_files(args.input) if os.path.isdir(args.input) else [args.input]

    for img_p in image_files:

        img = cv2.imread(img_p)
        detected_objects, out_im = predictor.recognize(img)

        if args.draw:
            bname = os.path.splitext(os.path.basename(img_p))[0]
            filename = os.path.join(args.output, f"out_{bname}.jpg")
            cv2.imwrite(filename, out_im)
            _logger.info(f"Saved result to {filename}")


if __name__ == "__main__":
    main()
