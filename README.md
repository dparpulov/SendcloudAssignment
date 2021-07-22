# Sendcloud "RSS scraper" assignment

The "RSS scraper" project was a technical assignment created for Sendcloud. Its aim was to assess my technical knowledge.

## Technical description

The project was developed using FastAPI which is a python framework for building APIs. The app can be ran through Docker by building an image and running it in a container by utilising the Docker file.

#### Requirements

- All of the requirements are mentioned in the requirements.txt file
- sqlite was used as a database to store the users, feeds and their items, as well as which feeds the users follow and which items they have read
- beautifulsoup was used to scrape the data from the rss feeds
- pytest was used to write the tests

## How to run

- Go in the project folder
- Open a cmd

Then do one of the following

- Run 'pip instsall -r requirements.txt'
- Run 'uvicorn main:app'

OR

- Run 'docker build -t rssScraper .'
- Run 'docker run -d --name 	rssContainer -p 8000:8000 rssScraper'

After that, you'll see it running and you can visit the API at:

- http://127.0.0.1:8000/
- http://127.0.0.1:8000/docs# - Swagger specification
- http://127.0.0.1:8000/redoc


## About the program

The "RRS scraper" is containerized with docker and you can:
- Follow and unfollow the different feeds
- See the items from the followed feeds
- See all the items of the different or a specific feed
- Read different items
- See which items a user has read or hasn't read yet from all or from a specific feed
- Feeds are automatically updated periodically

## Cool technical stuff

### To do

## Class design decisions

### To do

### Early design

![Brainstorm](/rss_scraper_brainstorming.jpg )

## Questions?

For further questions about the app, please refer to its codebase, where almost all functions are commented on and explained. For more information, please contact me at <dd.parpulov@gmail.com>.