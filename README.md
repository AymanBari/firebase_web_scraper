# A Firebase Web Scraper
Scraping firebase analytics dashboards for a dataset that lends itself to easier analysis. 

This project was written to provide some user-level analytics with Firebase's free analytics package. If you have a firebase subscription, the integration with Google's [BigQuery](https://cloud.google.com/bigquery) will provide a much richer source of data. 


## Background 
Assumptions 
* Each user will be identified by a unique user property 
* You have created a set of custom events that you are interested in tracking 

This script will produce a table with the following structure, for each day that it is run: 

|        |Event 1 | Event 2 | ... | Event N |
|--------| ------ |:-------:| ---:|--------:|
| User 1 |        |         |     |         |
| User 2 |        |         |     |         |
| ...    |        |         |     |         |
| User N |        |         |     |         |


## Required Libraries 
```python
import mysql.connector  # Access DB 
import selenium   # Browser automation (accessing required pages) 
import bs4        # Scrape   
import openpyxl # Store scraped data in an excel sheet 
import datetime # Log record dates 
import time     # Record script runtime 
```


## Steps 
This script takes the following steps: 

1. Open Browser 
2. Log in to the firebase account 
3. Pull the list of users from your DB (MySQL DB in this case) 
4. Access events summary page for each user 
5. Navigate to event detail pages (if events are logged) 
6. Scrape required data 
7. Store in spreadsheet 


## Functions 
```python 
open_browser_to_firebse() 
```
Opens a broweser via Selenium Webdriver. Hard coded to access [firebase.com](https://firebase.com)


```python 
sign_in_to_firebase()
```
In this implementation, credentials are hardcoded to log-in to your firebase account and access the relevant project. Ideally, this function should prompt the user to enter their password (see [getpass()](https://docs.python.org/2/library/getpass.html) module) 


```python 
get_list_of_users()
```
Pulls a list of user ids from your existing DB. These must match the unique user_properties of the user profiles you are looking to scrape from. Select query is hardcoded in this function. 


```python 
access_events_page_for_user(user_id)
```
Navigates the firebases events page. Filters for the user passed in the user_id parameter. 


```python 
check_for_logged_activities()
```
Excuted after ```access_events_page_for_user()``` method. Checks if current user has any logged events. Returns False if no events found. 


```python 
get_logged_events()
```
If ```check_for_logged_activities()``` returns True, this function returns a list of the events that have been logged. 


```python 
check_if_logged_events_are_required(logged_events, user_id)
```
Comapres the list of logged events (provided by ```get_logged_events()``` with a list of required events (assuming only a subset of all events are required for scraping). Comparison is made against a global dictionary with event names and corresponding URLs as key:value pairs. Calls ```scrape_data``` function for each required event. 


```python 
scrape_data(event)
```
Scrapes required data for the event parameter provided. 


```python 
store_in_spreadsheet(collected_data)
```
Stores collected data in a spreadsheet. 

