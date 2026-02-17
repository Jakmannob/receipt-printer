import glob
import os
import tomllib

import cv2
from PIL import Image


class Camera:

    def __init__(self, save_dir, config_file="devices.toml"):
        self.save_dir = save_dir
        self.device = self._load_camera()

    def _load_camera(self, config_file="devices.toml"):
        with open(config_file, "rb") as config_file:
            config = tomllib.load(config_file)
        dev = config["devices"]["camera"]["device"]

        if dev not in glob.glob("/dev/video*"):
            raise FileNotFoundError(
                "USB camera not configured! Please execute `configure_camera.py`!"
            )
        return dev

    def take_transform_and_save_image(
        self, alpha=1.2, beta=40, bw_threshold=-1, file_name="temp.jpg"
    ):
        frame = self.take_image()
        transformed = self.transform_image(
            frame, alpha=alpha, beta=beta, bw_threshold=bw_threshold
        )
        return self.save_image(transformed, file_name=file_name)

    def take_image(self):
        cap = cv2.VideoCapture(self.device, cv2.CAP_V4L2)
        ret, frame = cap.read()
        cap.release()

        if not ret:
            raise IOError("USB camera did not take a image")
        return frame

    def transform_image(self, frame, alpha=1.2, beta=40, bw_threshold=-1):
        # alpha is contrast (1.0-3.0)
        # beta is brightness (0-100)
        adjusted = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
        rotated = cv2.rotate(adjusted, cv2.ROTATE_90_CLOCKWISE)

        img = Image.fromarray(rotated)
        width = 512
        ratio = width / img.width
        img = img.resize((width, int(img.height * ratio))).convert("L")
        # Convert to clean black/white
        if bw_threshold >= 0:
            img = img.point(lambda x: 0 if x < bw_threshold else 255, "1")
        return img

    def save_image(self, img, file_name="temp.jpg"):
        save_path = os.path.join(self.save_dir, file_name)
        img.save(save_path)
        return save_path
