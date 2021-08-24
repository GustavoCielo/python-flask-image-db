from flask import Flask, jsonify
import os
from environs import Env
from kenzie.images import upload_files, get_files_by_type, download_file_by_type, download_as_zip

env = Env()
env.read_env()

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1000000

if not os.path.exists(env("FILES_DIRECTORY")):
    os.makedirs(env("FILES_DIRECTORY"))


@app.route("/", methods=["GET"])
def home():
    return "<h1>Hello Flask</h1>"


@app.post("/upload")
def upload():
    try:
        return upload_files()
    except:
        return {"msg": "O arquivo enviado precisa ser menor do que 1 MB"}, 413


@app.get("/files")
def list_files():
    """
    lista todos os arquivos no banco de imagens
    """
    try:
        return jsonify(os.listdir(env("FILES_DIRECTORY"))), 200
    except:
        return {"msg": "Não há arquivos a serem listados."}, 404


@app.get("/files/<string:type>")
def list_files_by_type(type: str):
    return get_files_by_type(type)


@app.get("/download/<string:file_name>")
def download(file_name: str):
    return download_file_by_type(file_name)


@app.get("/download-zip")
def download_dir_as_zip():
    return download_as_zip()
