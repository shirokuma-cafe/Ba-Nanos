from PIL import Image
from pathlib import Path

IMAGES = Path("/Users/cris/Desktop/Ba-Nanos/images")

for image in IMAGES.iterdir():
    pil_image = Image.open(image)
    new_image = pil_image.resize((512, 512))

    new_image.save(image)