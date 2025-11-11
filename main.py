import os
import shutil
import random

from dotenv import load_dotenv
load_dotenv(override=True)

os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

tmp = os.path.join(os.getcwd(), 'temp')
sts = os.getenv('APP_STATUS', 'development')

if not os.path.exists(tmp):
    os.mkdir(tmp)
    
if sts == 'production':
    os.environ["HF_HOME"] = tmp

from io import BytesIO
from formula import Formula
from fastapi import FastAPI, File, UploadFile, HTTPException

app = FastAPI()
frm = Formula()

@app.get(f'/')
async def index():
    return {
        'status'  : 'success',
        'message' : 'API is up and running'
    }

@app.post(f'/formula')
async def detect_formula(
    img: UploadFile = File(...)
):
    img_byte = await img.read()
    img_name = frm.get_random_filename()
    img_path = os.path.join(tmp, f'{img_name}.jpg')
    
    with open(img_path, 'wb') as fle:
        fle.write(img_byte)

    equation = frm.detect_formula([img_path])
    
    if (os.path.exists(img_path)):
        os.remove(img_path)    
    
    return {
        'status'   : 'success',
        'response' : equation,
        'message'  : 'Equation successfuly detected'
    }