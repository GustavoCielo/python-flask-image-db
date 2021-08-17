from flask import Flask, request, safe_join
import os
from datetime import datetime

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1000000

FILES_DIRECTORY = "./images/"

if not os.path.exists(FILES_DIRECTORY):
    os.makedirs(FILES_DIRECTORY)

@app.route("/", methods=["GET"])
def home():
    return "<h1>Hello Flask</h1>"


@app.post("/upload")
def upload():

    extension_types = ["gif", "jpg", "png"]
        
    try:

        # file = request.files["file"]

        file = request.files[list(request.files.keys())[0]]
        extension = file.filename.split('.')[-1]
        new_filename = file.filename.replace(" ", "_")
        
        if new_filename in os.listdir(FILES_DIRECTORY):
            return {"msg": "O arquivo ja existe no banco de dados"}, 409

        if extension in extension_types:
            file.save(f"{FILES_DIRECTORY}/{new_filename}")
            return {"msg": f"Envio realizado com sucesso, {new_filename}"}, 201
   
        return {"msg": "O arquivo precisa ser JPG, GIF ou PNG"}, 415
        
    except:
        return {"msg": "O arquivo enviado precisa ser menor do que 1 MB"}, 413



