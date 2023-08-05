import matplotlib.pyplot as plt

def plot_image(image):
    plt.figure(figsize=(12, 12))
    plt.imshow(image, cmap="gray")
    plt.axis("off")
    plt.show()


def plot_result(initial_image, image_compare, comparation_result: str):
    figure, axis = plt.subplots(nrows=1, ncols=2, figsize=(12, 12))
    figure.suptitle(f'** {comparation_result} **' )
    list_images = [initial_image, image_compare]
    list_titles = ["Initial image", "Compare image"]
    for ax, title, image in zip(axis, list_titles, list_images):
        ax.set_title(title)
        ax.imshow(image, cmap="gray")
        ax.axis("off")
    figure.tight_layout()
    figure.subplots_adjust(top=0.85)
    plt.show()


