# review scrapper with flaskapp
Context
Web scraping is the process of using bots to extract content and data from a website. Unlike screen scraping, which only copies pixels displayed onscreen, web scraping extracts underlying HTML code and, with it, data stored in a database. The scraper can then replicate entire website content elsewhere.

# Introduction
In this project, I have developed an api which extracts data from imdb website. You can get the data of higest voted reviews of any shows or movies from the project.


# The following steps have been used to build the web scraping project using Python and its ecosystem of libraries:

* Pick a website
 I have picked imdb website for scraping the reviews of the shows

* Use the requests library to download web pages
 Download and save web pages locally using the requests library.(opening a url)
 
* Use Beautiful Soup to parse and extract information
 Parse and explore the structure of downloaded web pages using Beautiful soup.

* Add the extracted information in a cloud database.
 I have used mongodb Database.
 
* Deploy the app in cloud platforms.
  I have used Heroku

