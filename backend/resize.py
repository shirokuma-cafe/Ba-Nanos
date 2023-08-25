from PIL import Image
from pathlib import Path

IMAGES = Path("../resize")
for image in IMAGES.iterdir():
    pil_image = Image.open(image)
    new_image = pil_image.resize((512, 512))

    new_image.save(f"../resize/{image}")