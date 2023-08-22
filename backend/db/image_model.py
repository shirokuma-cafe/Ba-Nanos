from io import BytesIO
from bson.binary import Binary
import matplotlib.pyplot as plt
from PIL import Image
from typing import Union
from pathlib import Path
from pymongo.collection import Collection
from pymongo import MongoClient
from dotenv import dotenv_values
conf = dotenv_values("../../.env")        

ROOT_DIR = Path(__file__).parent.parent.parent
def insert_style_image(style_name:str, image: Union[str, BytesIO], collection):
    """
    Inserts a style image into the collection, accepts a style name and buffer to upload
    """
    try:
        fmt = image.split(".")[1] # get format of image (jpg, png)
        im = Image.open(image)

        # Get bytes from image and save to memory
        image_bytes = BytesIO()
        im.save(image_bytes, format=fmt)

        mongo_collection: Collection = collection
        mongo_collection.insert_one({
            'style': style_name,
            'format': fmt,
            'data': image_bytes.getvalue()
        }
        )

    except FileNotFoundError as e:
        # Look for file in root directory if not in current directory
        print(f"error occured while accessing image {image}, with error {str(e)}")
        print(f"looking for file inside inside root directory")
        new_image = f"{ROOT_DIR}/{image}"
        fmt = new_image.split(".")[1] # get format of image (jpg, png)

        im = Image.open(new_image)

        #Convert the image into bytes and store it
        image_bytes = BytesIO()
        im.save(image_bytes, format='jpg')

        mongo_collection: Collection = collection
        mongo_collection.insert_one({
            'style': style_name,
            'format': fmt,
            'data': image_bytes.getvalue()
        }
        ).inserted_id

def get_style_image(style: str, collection):
    """
    Returns a style image based on specified style, this style is then applied to 
    input image
    """
    collection: Collection = collection
    style_image = collection.find_one({"style": style})

    # Get byte data from database
    image = Image.open(BytesIO(style_image['data']))
    
    return image
