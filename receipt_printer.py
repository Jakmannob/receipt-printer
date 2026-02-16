from escpos.printer import Usb
import cv2
from PIL import Image
import tomllib
import subprocess
import glob
import os


IMAGE_DIR = 'images'


class Printer:

    def __init__(self, config_file='devices.toml'):
        self.printer = self._load_printer(config_file)

    def _load_printer(self, config_file='devices.toml'):
        with open(config_file, 'rb') as config_file:
            config = tomllib.load(config_file)
        dev = config['devices']['printer']
        vid, pid = int(dev['vendor_id'], 16), int(dev['product_id'], 16)
        printer = Usb(vid, pid)
        if dev['paper_width'] == '58mm':
            printer.profile.profile_data['media']['width']['pixels'] = 384
        else:
            printer.profile.profile_data['media']['width']['pixels'] = 576
        return printer

    def cut(self):
        self.printer.cut()

    def print_image(self, path):
        image = Image.open(path).convert('L')
        self.printer.image(image)


class Camera:
    
    def __init__(self, save_dir, config_file='devices.toml'):
        self.save_dir = save_dir
        self.device = self._load_camera()

    def _load_camera(self, config_file='devices.toml'):
        with open(config_file, 'rb') as config_file:
            config = tomllib.load(config_file)
        dev = config['devices']['camera']['device']

        if dev not in glob.glob('/dev/video*'):
            raise FileNotFoundError(f'USB camera not configured! Please execute `configure_camera.sh`!')
        return dev
    
    def take_transform_and_save_image(self, alpha=1.2, beta=40, file_name='temp.jpg'):
        frame = self.take_image()
        transformed = self.transform_image(frame, alpha=alpha, beta=beta)
        return self.save_image(transformed, file_name=file_name)

    def take_image(self):
        cap = cv2.VideoCapture(self.device, cv2.CAP_V4L2)
        ret, frame = cap.read()
        cap.release()
    
        if not ret:
            raise IOError(f'USB camera did not take a image')
        return frame
    
    def transform_image(self, frame, alpha=1.2, beta=40, bw_threshold=-1):
        # alpha is contrast (1.0-3.0)
        # beta is brightness (0-100)
        adjusted = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
        rotated = cv2.rotate(adjusted, cv2.ROTATE_90_CLOCKWISE)

        img = Image.fromarray(rotated)
        width = 512
        ratio = width / img.width
        img = img.resize((width, int(img.height * ratio))).convert('L')
        # Convert to clean black/white
        if bw_threshold >= 0:
            img = img.point(lambda x: 0 if x < bw_threshold else 255, '1')
        return img
    
    def save_image(self, img, file_name='temp.jpg'):
        save_path = os.path.join(self.save_dir, file_name)
        img.save(save_path)
        return save_path


def take_image_and_print(camera, printer):
    save_path = camera.take_transform_and_save_image()
    printer.print_image(save_path)
    printer.cut()

if __name__ == '__main__':
    camera = Camera(IMAGE_DIR)
    printer = Printer()
    
    take_image_and_print(camera, printer)
    exit()
