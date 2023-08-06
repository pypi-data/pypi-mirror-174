from cv2 import rectangle
from face_recognition import face_locations
from face_recognition import face_encodings
from face_recognition import compare_faces
from face_recognition import face_distance

def _encode_image(image):
    return face_encodings(image)[0]

def _result_message(comparison_result: list, distance_images):
    result_message = ""
    if comparison_result[0] == True:
        result_message = f"The faces belong to the same person. Distance between faces: {distance_images}"
    else:
        result_message = f"The faces are of different people. Distance between faces: {distance_images}"
    return result_message.replace("[", "").replace("]", "")

def delimit_face(image):
    face_location = face_locations(image)[0]
    rectangle(image, (face_location[3], face_location[0]), (face_location[1], face_location[2]), (0,255,0), 2)
    return image

def confront_faces(initial_image, compare_image):
    init_img = _encode_image(initial_image)
    comp_img = _encode_image(compare_image)
    comparison = compare_faces([init_img], comp_img)[0]
    distance = face_distance([init_img], comp_img)[0]
    return comparison, distance

def confront_faces_message(initial_image, compare_image):
    init_img = _encode_image(initial_image)
    comp_img = _encode_image(compare_image)
    comparison = compare_faces([init_img], comp_img)
    distance = face_distance([init_img], comp_img)
    return _result_message(comparison, distance)


import load_img
image1 = load_img.get_image_file("E:\\Arquivos\Downloads\stark1.jpg")
#image1 = delimit_face(image1)
image2 = load_img.get_image_file("E:\\Arquivos\Downloads\stark2.jpg")
#image2 = delimit_face(image2)

print(confront_faces(image1, image2))

