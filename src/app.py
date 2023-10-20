import base64
import boto3
import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pathlib import Path
from typing import Union

ENV = os.environ["ENV"]
app = FastAPI(title="FastAPI app", version="0.0.1")


def return_images():
    if ENV == "test":
        session = boto3.Session(profile_name="personal")
    else:
        session = boto3.Session()
    s3 = session.client("s3")
    bucket = "fast-website"
    response = s3.list_objects_v2(Bucket=bucket, Prefix="pictures/")
    images = []
    for obj in response["Contents"]:
        if obj["Key"] != "pictures/":
            image = s3.get_object(Bucket=bucket, Key=obj["Key"])["Body"].read()
            image_64 = base64.b64encode(image).decode("utf-8")
            images.append(image_64)
    return images


@app.get("/", response_class=HTMLResponse)
def read_root():
    html_response = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Tu y Yo</title>
    </head>
    <body>
        <h1>Un album para los dos</h1>
    """
    images = return_images()
    for image in images:
        html_response += f'<img src="data:image/jpeg;base64,{image}" alt="Image">'
    html_response += "<h2>Te amo mi amor</h2>"
    html_response += "<h3>Esto sera mas bonito pronto</h3>"
    html_response += "<h4>No te imaginas las ganas que tengo de hacerte el amor duro, sucio y salvaje.</h4>"
    html_response += "</body></html>"
    return html_response

if __name__ == "__main__":
    import uvicorn
    
    if ENV == "test":
        uvicorn.run(f"{Path(__file__).stem}:app", host="0.0.0.0", port=8080, reload=True, log_level="info")
    else:
        uvicorn.run(app, host="0.0.0.0", port=8080)
