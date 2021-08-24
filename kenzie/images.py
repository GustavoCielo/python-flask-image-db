from flask import request, safe_join, send_from_directory, jsonify
import os
from environs import Env
env = Env()
env.read_env()


def upload_files():
    """
    Envia arquivos ao banco de imagens,
    verificando o tipo de extensão e o tamanho máximo permitido
    através da variável de ambiente
    """

    extension_types = ["gif", "jpg", "png"]

    file = request.files[list(request.files.keys())[0]]
    extension = file.filename.split('.')[-1]
    new_filename = file.filename.replace(" ", "_")

    if new_filename in os.listdir(env("FILES_DIRECTORY")):
        return {"msg": "O arquivo ja existe no banco de dados"}, 409

    if extension in extension_types:
        file.save(safe_join(env("FILES_DIRECTORY"), new_filename))
        return {"msg": f"Envio realizado com sucesso, {new_filename}"}, 201

    return {"msg": "O arquivo precisa ser JPG, GIF ou PNG"}, 415


def get_files_by_type(type: str):
    """
    Retorna uma lista com os arquivos determinados pelo query params
    """

    filtered_items = [
        item for item in os.listdir(env("FILES_DIRECTORY"))
        if item.split(".")[-1] == type
    ]

    if len(filtered_items) == 0:
        return {
            "msg": "Não há arquivos há serem listados por essa extensão"
        }, 404

    return jsonify(filtered_items), 200


def download_file_by_type(file_name: str):
    """
    Download de arquivos baseado na extensão do query param
    """

    filtered_item = [
        item for item in os.listdir(env("FILES_DIRECTORY"))
        if item.replace(" ", "_") == file_name
    ]

    if not filtered_item:
        return {"msg": "Arquivo inexistente"}, 404

    file = filtered_item[0]

    return send_from_directory(
        directory=f".{env('FILES_DIRECTORY')}",
        path=file,
        as_attachment=True
    )


def download_as_zip():
    """
    Download de arquivos como zip através de argumentos de compressão e tipo
    """

    if len(os.listdir(env("FILES_DIRECTORY"))) == 0:
        return {"msg": "Não há arquivos a serem baixados"}, 404

    compression_rate = request.args.get("compression_rate", 6)
    extension = request.args.get("file_type", None)

    if extension:
        filtered_items = [
            item for item in os.listdir(env("FILES_DIRECTORY"))
            if item.split(".")[-1] == extension
        ]
        if len(filtered_items) == 0:
            return {"msg": "Arquivo não existe"}, 404

        os.system(
            f'zip -{compression_rate} -r /tmp/images.zip {env("FILES_DIRECTORY")}/*{extension}'
        )
    else:
        os.system(
            f"zip -{compression_rate} -r /tmp/images.zip {env('FILES_DIRECTORY')}"
        )

    return send_from_directory(
        directory="/tmp",
        path="images.zip",
        as_attachment=True
    ), 200
