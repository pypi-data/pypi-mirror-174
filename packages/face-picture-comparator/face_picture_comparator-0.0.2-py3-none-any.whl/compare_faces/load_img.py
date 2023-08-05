from face_recognition import load_image_file

def get_image_file(image_file):
    image = load_image_file(image_file)
    return image