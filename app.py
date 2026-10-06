from fastapi import FastAPI, Form, Request, Response, File, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
import uvicorn
import os
import aiofiles
import json 
import csv
from src.helper import llm_pipeline
from io import BytesIO
from pypdf import PdfReader
import re

MAX_MB = 5
MAX_PAGES = 5

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/upload")
async def upload(request: Request, pdf_file: bytes = File(), filename: str = Form(...)):
    if len(pdf_file) > MAX_MB * 1024 * 1024:
        raise HTTPException(status_code=413, detail=f"File is too large. The limit is {MAX_MB} MB.")

    try:
        page_count = len(PdfReader(BytesIO(pdf_file)).pages)
    except Exception:
        raise HTTPException(status_code=400, detail="This file isn't a valid PDF.")

    if page_count > MAX_PAGES:
        raise HTTPException(status_code=400, detail=f"This PDF has {page_count} pages. The limit is {MAX_PAGES}.")

    base_folder = 'static/docs/'
    if not os.path.isdir(base_folder):
        os.mkdir(base_folder)
    pdf_filename = os.path.join(base_folder, filename)

    async with aiofiles.open(pdf_filename, 'wb') as f:
        await f.write(pdf_file)

    response_data = jsonable_encoder(json.dumps({"msg":'success',"pdf_filename": pdf_filename}))
    res = Response(response_data)
    return res

def clean_text(s):
    # turn literal "\u202f"-style codes into real characters
    s = re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), s)
    # swap special spaces and hyphens for plain ones
    s = s.replace("\u202f", " ").replace("\u00a0", " ").replace("\u2011", "-")
    # remove markdown bold and leading numbering
    s = s.replace("**", "")
    s = re.sub(r"^\s*\d+[\.\)]\s*", "", s)
    return s.strip()

def get_csv(file_path):
    ques_list, answer_generation_chain = llm_pipeline(file_path)
    base_folder = 'static/output/'
    if not os.path.isdir(base_folder):
        os.mkdir(base_folder)
    output_file = base_folder+"QA.csv"
    with open(output_file, "w", newline="", encoding="utf-8-sig") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Question", "Answer"]) #writing the header row

        for question in ques_list:
            question = clean_text(question)
            print("Question:", question)
            answer = answer_generation_chain.invoke(question)
            answer = clean_text(answer)
            print("Answer:", answer)
            print("---------------------------------------\n\n")

            #save answer to csv file
            csv_writer.writerow([question, answer])

    return output_file

@app.post("/analyze")
async def analyze(request: Request, pdf_filename: str = Form(...)):
    output_file = get_csv(pdf_filename)
    response_data = jsonable_encoder(json.dumps({"output_file": output_file}))
    res = Response(response_data)
    return res

if __name__ == "__main__":
    uvicorn.run("app:app", host='0.0.0.0', port=8000, reload=True)