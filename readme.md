This is the cloud environment for our jobstreet scraper hosted on google cloud. Built with Next, React, FastAPI, Selenium, and Pytorch sentence-transformers. The app scrapes from 'ph.jobstreet.com' weekly, and compares these job listings against the user's resume. The match is computed by cosine similarity, ignoring magnitude. The app then outputs the top matches by descending order.

The app is running on jobmatcherai.netlify.app, but due to budget constraints and limitations the app will only remain online until January 2026 or so. The app may take a few minutes to compute for job matches because it is deployed on a less powerful instance, and the code is to be optimized. 

The local environment exists in branch dev/local-environment for testing.


OPTIMIZATIONS (main):

Avoid creation of embeddings per user request.

Solutions:

Let the scraper handle the creation of the embeddings by adding them as a property in the element in json. (potential issue: may exhaust resources in the instance)
