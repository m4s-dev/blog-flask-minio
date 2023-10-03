from flask import Flask, request, redirect
from werkzeug.utils import secure_filename
from minio import Minio
import os

ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif", "xlsx", "mp4", "zip"}
ACCESS_KEY = os.environ.get("MINIO_ROOT_USER")
SECRET_KEY = os.environ.get("MINIO_ROOT_PASSWORD")
BUCKET_NAME = os.environ.get("MINIO_BUCKET")
MINIO_API_HOST = os.environ.get("MINIO_ENDPOINT")


def upload_object(filename, data, length):
  try:
    client = Minio(MINIO_API_HOST, ACCESS_KEY, SECRET_KEY, secure=False)

    # Make bucket if not exist.
    found = client.bucket_exists(BUCKET_NAME)
    if not found:
        client.make_bucket(BUCKET_NAME)
    else:
        print(f"Bucket {BUCKET_NAME} already exists")

    client.put_object(BUCKET_NAME, filename, data, length)
    print(f"{filename} is successfully uploaded to bucket {BUCKET_NAME}.")
    return True
  except Exception as e:
    print(f"Error uploading {filename} to bucket {BUCKET_NAME}. Error: {e}")
    return False


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

@app.route("/", methods=["GET", "POST"])
def upload_file():
    message = ""

    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
           message = "<span class='error-message'>No se seleccionó ningún archivo.</span>"
           return render_template(message)
        file = request.files["file"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
           message = "<span class='error-message'>No se seleccionó ningún archivo.</span>"
        elif not allowed_file(file.filename):
           message = "<span class='error-message'>Tipo de archivo no permitido.</span>"
        else:
            filename = secure_filename(file.filename)
            size = os.fstat(file.fileno()).st_size
            success = upload_object(filename, file, size)
            if success:
                message = "<span class='success-message'>Archivo subido con éxito.</span>"
            else:
                message = "<span class='error-message'>Error al subir el archivo.</span>"

    return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>UPLOAD</title>
          <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                padding: 50px;
                text-align: center;
            }}
            h1 {{
                color: #333;
            }}
            .success-message {{
                color: green;
                font-weight: bold;
            }}
            .error-message {{
                color: red;
                font-weight: bold;
            }}
            form {{
                background-color: #fff;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            input[type=file], input[type=submit] {{
                margin-top: 10px;
            }}
          </style>
        </head>
        <body>
          <h1>Upload file to minio bucket</h1>
          {message}
          <form method=post enctype=multipart/form-data>
            <input type=file name=file>
            <br>
            <input type=submit value=Upload>
          </form>
        </body>
        </html>
        """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)