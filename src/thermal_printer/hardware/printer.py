from escpos.printer import Usb
from PIL import Image
import tomllib


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
