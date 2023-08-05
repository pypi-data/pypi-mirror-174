from cv2 import cvtColor, COLOR_BGR2RGB
from face_recognition import load_image_file


def load_image_file(image_file):
    image = load_image_file(image_file)
    image = cvtColor(image, COLOR_BGR2RGB)
    return image