import base64
import cv2
import io
import numpy as np
import os
import imageio

def pil_to_cv2(pil_image):
    numpy_image = np.array(pil_image)
    bgr_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
    
    return bgr_image

def pil_to_b64(img):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")  # or format="JPEG", etc.

    # Get the bytes value
    img_bytes = buffered.getvalue()
    return base64.b64encode(img_bytes).decode('utf-8')

def display_image(image):
    cv2.imshow("controlnet", pil_to_cv2(image))
    cv2.waitKey(100)

def export_image(image, file_path):
    dirPath = os.path.dirname(file_path)
    os.makedirs(dirPath, exist_ok=True)

    image.save(file_path)

def export_movie(images, fps, output_file):
    with imageio.get_writer(output_file, mode='I', fps=fps) as writer:  # adjust fps as needed
        for pil_image in images:
            # Convert the PIL image to a numpy array
            numpy_image = np.array(pil_image)
            writer.append_data(numpy_image)