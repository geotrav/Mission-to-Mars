# Mission-to-Mars

## Purpose

The purpose of this project is to add Mars Hemipshere images via web scraping and add titles and image urls to the Mongo database.  These image scrapes will them be added to the exisiting HTML page for display.

### Results

1. Code was added to the [Python Scraping](/scraping.py) file to visit the Mars hemisphere website and then extract the title and url via an iterative process to click on images and grab titles and image urls.

2. Code then places the titles and urls in the Mongo database.  Here they are called upon a web page button click that pulls the fresh Mars data from the associated websites and stores the data in the Mongo DB.

3. HTML index file then refreshes the pages and populates with the data pull by querying the Mongo DB.

4. Underlining and additional formatting using Bootstrap was applied to the HTML code to make it more easily viewed on mobile devices.

### Summary

The final copy can be run by running the Python app.py file while having the Mongo DB running.  Once launch in a web browser the user can click the scrape new data and pull up to date data for the different sites.  The Mars hemispheres are avaiale below the original code. 