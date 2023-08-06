# face_picture_comparator

## Description. 

The package face_picture_comparator is used to:

	- Delimit face
	- Confront faces
	- Result confront faces
	- Plot image
	- Plot result
	- Get image file

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install face_picture_comparator

```bash
pip install face_picture_comparator
```

## Usage

```python
from face_picture_comparator import load_img

image = load_img.get_image_file("my_image.jpg")
image = load_img.delimit_face(image)

# delimit_face returns an image with a rectangle delimiting the first face detected in the input image

# the image containing the contour of the face should not be used as input to face comparison methods 
# (confront_faces_message and confront_faces)
```

```python
from face_picture_comparator import load_img
from face_picture_comparator import comparation
from face_picture_comparator import plot

image = load_img.get_image_file("my_image.jpg")
image_compare = load_img.get_image_file("other_image.jpg")
message_result = comparation.confront_faces_message(image, image_compare)

# result_confront_faces returns a string informing whether or not the faces belong to the same person and the distance between them

comparison_result = comparation.confront_faces(image, image_compare)
# returns a tuple where the first value is a boolean, which says whether or not the faces belong to the same person, and the second 
# value is a float that represents the distance between the faces

plot.plot_result(image, image_compare, message_result)

# plot_result displays the images and the massage using matplotlib library
```

```python
from face_picture_comparator import load_img
from face_picture_comparator import plot
image = load_img.get_image_file("my_image.jpg")
plot.plot_image(image)

# plot_image displays the image using matplotlib library
```

## Author
Ronaldo Nunes

## License
[MIT](https://choosealicense.com/licenses/mit/)