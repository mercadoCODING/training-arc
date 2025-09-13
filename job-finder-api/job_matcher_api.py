#fastapi endpoint
#takes two files: resume.pdf and job_listings.json
#returns sorted json by cosine similarty

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PyPDF2 import PdfReader
import io
import json


from sentence_transformers import SentenceTransformer, util

#load pretrained sentence transformer model
#model = SentenceTransformer('all-MiniLM-L6-v2') #faster and lightweight
model = SentenceTransformer('all-mpnet-base-v2') #more accurate

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/find_highest_cos_sim")
async def find_highest_cos_sim(resume_pdf: UploadFile = File(...), job_listings_json: UploadFile = File(...)): #upload two files, pdf and json

    'For resume_pdf handling'

    #check if pdf
    if resume_pdf.content_type != "application/pdf":
        return JSONResponse(content={"error":"Please upload PDF"}, status_code=400)
    
    # Read file into memory
    pdf_bytes = await resume_pdf.read()

    #wrap in BytesIO so pdfreader() can use it
    pdf_stream = io.BytesIO(pdf_bytes)

    reader = PdfReader(pdf_stream)

    resume_text = ""

    for page in reader.pages:
        resume_text += page.extract_text() or "" #if page.extract_text() returns None, concatenate with empty string instead

    
    'for job_listings_json handling'

    json_bytes = await job_listings_json.read()
    job_listings = json.loads(json_bytes.decode("utf-8")) #since json upload will be a list of dictionaries, job_listings becomes list of dicts

    #convert resume into tensors/embeddings
    resume_embedding = model.encode(resume_text, convert_to_tensor=True) 

    #unpacks title and description from each job listing into one string element
    #then converts that singular string into embeddings
    #job_embeddings is technically only one tensor (not a list of embeddings), but each row in the tensor is one job embedding, so it acts like a list
    job_embeddings = model.encode([f"{job['title']}: {job['description']}" for job in job_listings], convert_to_tensor=True)

    #similarly to job_embeddings, cosine_scores acts as a list of scores but is a tensor where each row is a cosine score.
    cosine_scores = util.cos_sim(resume_embedding, job_embeddings)
    

    # Convert cosine scores tensor into a Python list of floats
    cosine_scores_list = cosine_scores[0].tolist()

    # Attach cosine scores to jobs dicts in job_listings with new cosine_score key
    for job, score in zip(job_listings, cosine_scores_list): 
        job["cosine_score"] = score

    # sort job_listings by cosine_score in descending order and save to sorted_job_listings
    sorted_job_listings = sorted(job_listings, key=lambda job: job["cosine_score"], reverse=True)

    # fastapi automatically converts returned python objects into a JSON response
    return sorted_job_listings










    


