from flask import Flask, request, Response, jsonify, render_template
from io import BytesIO
import os
import torchvision.models as models
import torch
from PIL import Image
from pathlib import Path
from db.collection_model import CollectionManager
from db.user_model import create_user
from NST import image_loader, run_style_transfer, imshow
#from dotenv import dotenv_values
from flask_cors import CORS, cross_origin
from uuid import uuid4
import base64
import matplotlib.pyplot as plt

# Access connectiong string environment variable
URI = os.environ["MONGO_URI"]
app = Flask(__name__, template_folder="../frontend/")
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})

# Size of image, input and style image must be of same size
imsize = 512
cnn = models.vgg19(pretrained=True).features.eval()

cnn_normalization_mean = torch.tensor([0.485, 0.456, 0.406])
cnn_normalization_std = torch.tensor([0.229, 0.224, 0.225])

ROOT_DIR = Path(__file__).parent.parent
STYLE_IMAGE_DIR = f"{ROOT_DIR}/style_images"
OUTPUT_IMAGE_DIR = f"{ROOT_DIR}/outputs"
print(Path(STYLE_IMAGE_DIR).exists())

collection_manager = CollectionManager(URI)
style_collection = collection_manager.get_styles_collection()
user_collection = collection_manager.get_user_collection()

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")

# Health status check of backend
@app.route("/ping", methods=["GET"])
def index():
    return Response("Server is running", status=200)

@app.route("/register", methods=["GET", "POST"])
def register():
    # Get form data
    form_data = request.form

    username = form_data["username"]
    password = form_data["password"]

    return create_user(username, password, collection=user_collection)

@app.route("/process", methods=["POST"])
@cross_origin()
def process_image():
    data = request.form
    file = request.files['file']
    ext = data['extension']
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

    #process output image using PyTorch's Neural Style Transfer
    print(input_image)
    tensor_image = run_style_transfer(cnn=cnn, normalization_mean=cnn_normalization_mean,
    normalization_std=cnn_normalization_std, content_img=content_image, style_img=style_image,input_img=input_image)

    # Convert output image from Tensor into PIL image
    image:Image = imshow(tensor_image)
    #image.save(f"{OUTPUT_IMAGE_DIR}/test1.jpg")
    buffer = BytesIO()
    # Save image to BytesIO
    image.save(buffer, 'jpeg')

    buffer.seek(0)
    data = buffer.read()
    data = base64.b64encode(data).decode()

    #Remove temporary user file after succesfully processing
    os.remove(f"image{image_id}.{ext}")

    return jsonify({
        'message': 'success',
        'format': ext,
        'data': data
    })
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
