from thermal_printer import Camera, Printer

IMAGE_DIR = "images"
CONFIG_FILE = "devices.toml"


def take_image_and_print(camera, printer):
    save_path = camera.take_transform_and_save_image()
    printer.print_image(save_path)
    printer.cut()


if __name__ == "__main__":
    camera = Camera(IMAGE_DIR, config_file=CONFIG_FILE)
    printer = Printer(config_file=CONFIG_FILE)
    take_image_and_print(camera, printer)
    exit()
