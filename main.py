from typing import Union
from data_batik import data as data_batik
from fastapi import FastAPI, UploadFile, File, HTTPException
import requests

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


app = FastAPI()


def search_by_name(name):
    for item in data_batik:
        if item['name'] == name:
            return item
    return None


@app.post("/recognize")
async def recognize_image(image: UploadFile = File(...)):
    url = 'https://batikita-ml-it35sd3wyq-et.a.run.app/recognize'
    files = {'image': (image.filename, image.file, image.content_type)}

    try:
        response = requests.post(url, files=files)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

    # try:
    #     response = requests.post(url, files=files)
    #     result = (response.json())
    #     batik = search_by_name(result['result'])
    #     if batik is None:
    #         raise HTTPException(status_code=404, detail="Batik not found")
    #     return {
    #         "data": batik
    #     }
    # except requests.exceptions.RequestException as e:
    #     return {"error": str(e)}


@app.get("/getDetail")
async def getDetail(name: str):
    batik = search_by_name(name)
    try:
        if batik is None:
            raise HTTPException(status_code=404, detail="Batik not found")
        return {
            "data": batik
        }
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
