from flask import Flask, request, Response, jsonify, render_template
from io import BytesIO
from PIL import Image
from pymongo.errors import OperationFailure
from db.collection_model import CollectionManager
from db.user_model import create_user
from dotenv import dotenv_values
from flask_cors import CORS, cross_origin
from db.image_model import get_style_image
import base64

conf = dotenv_values("../.env")
app = Flask(__name__, template_folder="../templates/")
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})

collection_manager = CollectionManager( "mongodb+srv://bnanos-user:LeWIpAO2oQ9uMFgg@bananos.w7ajfnm.mongodb.net/?retryWrites=true&w=majority")
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
    mimetype = file.mimetype
    style = data["style"]

    # Get respective style image from database (expressionist, abstract, sketch, etc)
    style_image = get_style_image(style, style_collection)

    input_image = Image.open(file.stream)

    buffer = BytesIO()
    style_image.save(buffer, 'png')
    buffer.seek(0)
    #Process output image
    #Algorithm goes here

    #Read bytes from image
    data = buffer.read()
    data = base64.b64encode(data).decode()
    return jsonify({
        'message': 'success',
        'format': input_image.format,
        'data': data
    })
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)  
