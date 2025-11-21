This is the cloud environment for our jobstreet scraper hosted on google cloud. Built with Next, React, FastAPI, Selenium, and Pytorch sentence-transformers. The app scrapes from 'ph.jobstreet.com' weekly, and compares these job listings against the user's resume. The match is computed by cosine similarity, ignoring magnitude. The app then outputs the top matches by descending order.

The app is running on jobmatcherai.netlify.app, but due to budget constraints and limitations the app will only remain online until January 2026 or so.

The local environment exists in branch dev/local-environment for testing.