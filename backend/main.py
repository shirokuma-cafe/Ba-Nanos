import base64
import os
from io import BytesIO
from pathlib import Path
from uuid import uuid4

import matplotlib.pyplot as plt
import torch
import torchvision.models as models
from dotenv import dotenv_values
from flask import Flask, Response, jsonify, render_template, request
from flask_cors import CORS, cross_origin
from PIL import Image

from .db.collection_model import CollectionManager
from .db.user_model import create_user
from .NST import image_loader, imshow, run_style_transfer

# Access connection string environment variable
URI = os.environ["MONGO_URI"]
app = Flask(__name__, template_folder="../frontend")
cors = CORS(app, resource={r"/*": {"origins": "*"}})

# Size of image, input and style image must be of same size
imsize = 512
cnn = models.vgg19(pretrained=True).features.eval()

cnn_normalization_mean = torch.tensor([0.485, 0.456, 0.406])
cnn_normalization_std = torch.tensor([0.229, 0.224, 0.225])

ROOT_DIR = Path(__file__).parent.parent
STYLE_IMAGE_DIR = f"{ROOT_DIR}/style_images"
IMAGES_DIR = f"{ROOT_DIR}/backend/static/images"

collection_manager = CollectionManager(URI)
style_collection = collection_manager.get_styles_collection()
user_collection = collection_manager.get_user_collection()


@app.route("/", methods=["GET", "POST"])
def home():
    images = [im for im in os.listdir(IMAGES_DIR)]
    return render_template("index.html", user_image=images)


@app.route("/ping", methods=["GET"])
def index():
    """
    Validates that the server is up and running.
    """
    return Response("Server is running", status=200)


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security inside create_user function.
    """
    # Get form data
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not username:
            return "Username is required"
        elif not password:
            return "Password is required"

        return create_user(username, password, collection=user_collection)


@app.route("/process", methods=["POST"])
@cross_origin()
def process_image():
    """Processes an input image using PyTorch's Neural Style Transfer (NST)
    and returns a transformed image with a specified style, image is processed in the frontend as base46 encoded bytes.
    """

    # Access form data: image stream, image extension and style
    data = request.form
    file = request.files["file"]
    ext = data["extension"]
    mimetype = file.mimetype
    style = data["style"]

    # Tag content image with a uuid for deletion afterwards
    image_id = str(uuid4())

    # Get respective style image from directory
    style_image = image_loader(f"{STYLE_IMAGE_DIR}/{style}.jpg")
    input_image = Image.open(file.stream)
    resized = input_image.resize((512, 512))

    # resize and save user's image to match style's image size.
    resized.save(f"image{image_id}.{ext}")

    # Load input image (user's image)
    content_image = image_loader(f"image{image_id}.{ext}")
    input_image = content_image.clone()

    # process output image using PyTorch's Neural Style Transfer
    print(input_image)
    tensor_image = run_style_transfer(
        cnn=cnn,
        normalization_mean=cnn_normalization_mean,
        normalization_std=cnn_normalization_std,
        content_img=content_image,
        style_img=style_image,
        input_img=input_image,
    )

    # Convert output image from Tensor into PIL image
    image: Image = imshow(tensor_image)
    # image.save(f"{OUTPUT_IMAGE_DIR}/test1.jpg")
    buffer = BytesIO()
    # Save image to BytesIO
    image.save(buffer, "jpeg")

    buffer.seek(0)
    data = buffer.read()
    data = base64.b64encode(data).decode()

    # Remove temporary user file after successfully processing
    os.remove(f"image{image_id}.{ext}")

    return jsonify({"message": "success", "format": ext, "data": data})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
