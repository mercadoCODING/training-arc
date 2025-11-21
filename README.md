This is our app's local environment. A json list of 1000 jobs from ph.jobstreet.com exists inside the data folder. 

SETUP:

inside the job-finder-api directory, run `uvicorn job_matcher_api:app` to start the FastAPI endpoint that calculates the cosine similarity of the user's resume and the job listings.
inside the frontend folder, run `npm install` then `npm run dev` to start the dev server.

The app is to be optimized. It may take a few minutes to compute for matches depending on your machine. 

