#fastapi endpoint
#takes two files: resume.pdf and job_listings.json
#returns sorted json by cosine similarty
#NEW: Also supports fetching job_listings directly from Google Cloud Storage

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PyPDF2 import PdfReader
from google.cloud import storage
import io
import json
from typing import Optional

from sentence_transformers import SentenceTransformer, util

#load pretrained sentence transformer model
#model = SentenceTransformer('all-MiniLM-L6-v2') #faster and lightweight
model = SentenceTransformer('all-mpnet-base-v2') #more accurate

app = FastAPI(title="Job Matcher API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_latest_jobs_from_gcs(bucket_name: str = "jobstreet-scraper-478308-scraped-data"):
    """
    Fetch the latest scraped jobs from Google Cloud Storage
    Returns list of job dictionaries
    """
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        
        # List all blobs in the scrapes folder
        blobs = list(bucket.list_blobs(prefix="scrapes/all_jobs_"))
        
        if not blobs:
            return None
        
        # Sort by creation time to get the latest file
        latest_blob = sorted(blobs, key=lambda x: x.time_created, reverse=True)[0]
        
        # Download and parse JSON
        json_data = latest_blob.download_as_text()
        jobs = json.loads(json_data)
        
        return jobs
    
    except Exception as e:
        print(f"Error fetching jobs from GCS: {e}")
        return None

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Job Matcher API", "status": "active", "version": "1.0"}

@app.get("/jobs")
async def get_all_jobs():
    """Get all jobs from Google Cloud Storage"""
    jobs = get_latest_jobs_from_gcs()
    
    if not jobs:
        return JSONResponse(
            content={"error": "No jobs found in Cloud Storage"}, 
            status_code=404
        )
    
    return {"total_jobs": len(jobs), "jobs": jobs}

@app.post("/find_highest_cos_sim")
async def find_highest_cos_sim(
    resume_pdf: UploadFile = File(...), 
    job_listings_json: UploadFile = File(None)  # Made optional
):
    """
    Original endpoint - upload two files: pdf and json
    NEW: job_listings_json is now optional - if not provided, fetches from GCS automatically
    """

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
    
    # NEW: If job_listings_json not provided, fetch from GCS
    if job_listings_json is None:
        print("No JSON uploaded, fetching from Google Cloud Storage...")
        job_listings = get_latest_jobs_from_gcs()
        
        if not job_listings:
            return JSONResponse(
                content={"error": "No job listings provided and none found in Cloud Storage"}, 
                status_code=400
            )
    else:
        # Original logic - use uploaded JSON
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

@app.post("/match_with_gcs")
async def match_with_gcs(resume_pdf: UploadFile = File(...)):
    """
    NEW ENDPOINT: Simplified endpoint that only requires resume PDF
    Automatically fetches latest job listings from Google Cloud Storage
    """
    
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

    
    'Fetch job_listings from Google Cloud Storage'
    
    job_listings = get_latest_jobs_from_gcs()
    
    if not job_listings:
        return JSONResponse(
            content={"error": "No job listings found in Cloud Storage"}, 
            status_code=404
        )

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
    return {
        "total_jobs": len(sorted_job_listings),
        "top_matches": sorted_job_listings[:20],  # Return top 20 matches
        "all_matches": sorted_job_listings  # All jobs sorted by score
    }