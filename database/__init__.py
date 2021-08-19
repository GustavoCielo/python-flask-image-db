from flask import Flask, request, safe_join, jsonify, send_from_directory
import os

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1000000

FILES_DIRECTORY = "./images/"
app.config["UPLOAD_FOLDER"] = FILES_DIRECTORY
app.config["ALLOWED_EXTENSIONS"] = ["jpg", "png", "gif"]


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
            file.save(safe_join(FILES_DIRECTORY, new_filename))
            return {"msg": f"Envio realizado com sucesso, {new_filename}"}, 201

        return {"msg": "O arquivo precisa ser JPG, GIF ou PNG"}, 415

    except:
        return {"msg": "O arquivo enviado precisa ser menor do que 1 MB"}, 413


@app.get("/files")
def list_files():
    try:
        return jsonify(os.listdir(FILES_DIRECTORY)), 200
    except:
        return {"msg": "Não há arquivos a serem listados."}, 404


@app.get("/files/<string:type>")
def list_files_by_type(type: str):

    filtered_items = [
        item for item in os.listdir(FILES_DIRECTORY)
        if item.split(".")[-1] == type
    ]

    if len(filtered_items) == 0:
        return {
            "msg": "Não há arquivos há serem listados por essa extensão"
        }, 404

    return jsonify(filtered_items), 200


@app.get("/download/<string:file_name>")
def download(file_name: str):

    filtered_item = [
        item for item in os.listdir(FILES_DIRECTORY)
        if item.replace(" ", "_") == file_name
    ]
    file = filtered_item[0]

    if not file:
        return {"msg": "Arquivo inexistente"}, 404

    return send_from_directory(
        directory=f".{FILES_DIRECTORY}",
        path=file,
        as_attachment=True
    )


@app.get("/download-zip")
def download_dir_as_zip():

    if len(os.listdir(FILES_DIRECTORY)) == 0:
        return {"msg": "Não há arquivos a serem baixados"}, 404

    compression_rate = request.args.get("compression_rate", 6)
    extension = request.args.get("file_type", None)
    if extension:
        filtered_items = [
            item for item in os.listdir(FILES_DIRECTORY)
            if item.split(".")[-1] == extension
        ]
        if extension in filtered_items:
            os.system(
                f"zip -{compression_rate} -r /tmp/images.zip {FILES_DIRECTORY}/*{extension}"
            )
        else:
            return {"msg": "Arquivo não existe"}, 404
    else:
        os.system(
            f"zip -{compression_rate} -r /tmp/images.zip {FILES_DIRECTORY}"
        )

    return send_from_directory(
        directory="/tmp",
        path="images.zip",
        as_attachment=True
    ), 200
