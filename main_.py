from typing import Optional, List
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder

import pandas as pd

app = FastAPI()


class Item(BaseModel):
    user_name: dict


@app.post("/files/")
async def create_file(files: List[bytes] = File(...)):
    df = pd.read_csv("Python Scripts\Dummy_Dataset.csv")
    df.duplicated().sum()
    dup1 = []
    for i, j in zip(df.duplicated().values, df.duplicated().index.values):
        if i:
            dup1.append(j)
    df_dup1 = df.loc[dup1]
    json_compatible_item_data = jsonable_encoder(df_dup1)
    return JSONResponse(content=json_compatible_item_data)
    # return {"file_sizes": [file for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    return {"filenames": [file.filename for file in files]}


@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
