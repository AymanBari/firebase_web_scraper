# Firebase_scraper_clean_SRC	
# Version_1.2            		  


### IMPORT REQUIRED LIBRARIES 
import time
import openpyxl
from openpyxl import Workbook
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error
import datetime


### FUNCTIONS 
def get_list_of_users():
    # print('get_list_of_users')
    try:
        connection = mysql.connector.connect(
                                             #PARAMS FOR YOUR DB HERE 
                                            )
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL database... MySQL Server version on ", db_Info)
            sql_select_Query = "SELECT id FROM users_tbl" # QUERY THAT WORKS FOR YOUR DB STRUCT  
            cursor = connection.cursor()
            cursor.execute(sql_select_Query)
            record = cursor.fetchall()
            # print(record)
            # print(len(record))
            list_of_records = []

            for r in range(len(record)):
                x = int(record[r][0])
                list_of_records.append(x)
            print(list_of_records)
            print(len(list_of_records))
            # print ("Your connected to - ", record)
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        # closing database connection.
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    return list_of_records


def open_browser_to_firebse():
    print('open_browser_to_firebse')
    driver.get('https://firebase.com')
    try:
        element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@data-label='Sign in button']")))
    except:
        print("an error occured while loading the page - could not find sign-in button")
        

def sign_in_to_firebase():
    print('sign_in_to_firebase')
    # Log in credentials
    username = "YOUR USER NAME HERE"
    pwd = "YOUR PASSWORD HERE"
    # TODO - check if the current page has the correct URL
    sign_in_link = driver.find_element_by_xpath("//a[@data-label='Sign in button']")
    sign_in_link.click()
    time.sleep(3)

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='identifierId']")))
        input_email = driver.find_element_by_xpath("//input[@id='identifierId']")
        input_email.clear()
        input_email.send_keys(username)
    except:
        print("Could not find the input field for username - sign_in_to_firebase()")

    next_button = driver.find_element_by_xpath("//div[@role='button'][@id='identifierNext']")
    next_button.click()
    time.sleep(3)

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
        input_pwd = driver.find_element_by_xpath("//input[@type='password']")
        input_pwd.clear()
        input_pwd.send_keys(pwd)
    except:
        print("Could not find the input field for password - sign_in_to_firebase()")
    time.sleep(1)
    next_button = driver.find_element_by_xpath("//div[@role='button'][@id='passwordNext']")
    next_button.click()


def set_url_for_current_user_id(event, user_id):
    print('set_url_for_current_user_id')
    
    # If all event urls are of the same length use OR operator in if 
    if event == 'EVENT_1':
        print('EVENT_1')
        app_launch_url = event_page_urls['EVENT_1']
        print(app_launch_url)
        # Update to match your url first half/second half indices  
        first_half = app_launch_url[:180]
        second_half = app_launch_url[190:]
        user = user_id
        url = first_half + user + second_half
        print(url)
        return url

    # If event page urls differ in length / position of parameters
    elif event == 'EVENT_2':
        print('EVENT_2')
        app_launch_url = event_page_urls['EVENT_2']
        print(app_launch_url)
        # Update to match your url first half/second half indices  
        first_half = app_launch_url[:185]
        second_half = app_launch_url[195:]
        user = user_id
        url = first_half + user + second_half
        print(url)
        return url
    
    elif event == 'EVENT_3':
        print('EVENT_3')
        app_launch_url = event_page_urls['EVENT_3']
        print(app_launch_url)
        # Update to match your url first half/second half indices  
        first_half = app_launch_url[:190]
        second_half = app_launch_url[200:]
        user = user_id
        url = first_half + user + second_half
        print(url)
        return url

    else:
	    print("could not match event", event, " to any url. ")


def get_logged_events():
    print("get_logged_events")
    logged_events = []
    driver.switch_to_default_content()
    iframes = driver.find_elements_by_tag_name("iframe")
    driver.switch_to.frame(iframes[0])
    try:
        element_present = WebDriverWait(driver, 1).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//*[@class="first-col event-name ng-binding"]')
            )
        )
        html = driver.execute_script('return document.documentElement.innerHTML')
        soup = BeautifulSoup(html, 'html.parser')
        # print(soup.text[:500], "\n")
        print("number of event rows found: ", 
              len(soup.findAll('div', {"class": "first-col event-name ng-binding"}))
             )
        if len(soup.findAll('div', {"class": "first-col event-name ng-binding"})) != 0:
            contents_of_page = soup.findAll('div', {"class": "first-col event-name ng-binding"})
            for content in range(len(contents_of_page)):
                content = contents_of_page[content]
                content = content.text.strip()
                logged_events.append(content)
            print(logged_events)
            print("\n")

        return(logged_events)

    except:
        print("Could not find any rows on - all events page. ")

        
def check_if_logged_events_are_required(logged_events, user_id):
    print('check_if_logged_events_are_required')
    required_events = event_page_urls.keys()    # check if the logged activities are required
    for event in logged_events:
        if event in required_events:
            url = event_page_urls[event]        # Gets the base url for that page
            url = set_url_for_current_user_id(event, user_id)       # Adds the current user's id to it
            driver.get(url)          # Load the page for that metric
            time.sleep(10)           # Wait for the page to load
            scrape_data(event)
        else:
            print(event, " is not a required event. ")


def scrape_data(event):
    ## FOR EVENTS WITHOUT PARAMETERS 
    if event == 'EVENT_1' or event == 'EVENT_2' or event == 'EVENT_3':  
        print('event is: ', event)
        driver.switch_to.default_content()
        iframes = get_list_of_all_frames_on_page()
        driver.switch_to.frame(iframes[0])
        time.sleep(3)
        try:
            element_present = WebDriverWait(driver, 1).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//*[@class="value ng-scope layout-row"]')
                )
            )
            html = driver.execute_script('return document.documentElement.innerHTML')
            soup = BeautifulSoup(html, 'html.parser')
            # print(soup.text[:500], "\n")
            print("number of event rows found: ",
                  len(soup.findAll('div', {"class": "value ng-scope layout-row"})))
            scraped = []
            if len(soup.findAll('div', {"class": "value ng-scope layout-row"})) != 0:
                contents_of_page = soup.findAll('div', {"class": "value ng-scope layout-row"})
                for content in range(len(contents_of_page)):
                    content = contents_of_page[content].span
                    content = content.text.strip()
                    scraped.append(content)
                print(scraped)
                print("\n")
                # Store in collected_data object
                if event == 'EVENT_1':
                    collected_data['EVENT_1'] = scraped[0] # Use the index for the data you need 
                elif event == 'EVENT_2':
                    collected_data['EVENT_2'] = scraped[0] # Edit index to requirement 
                elif event == 'EVENT_3':
                    collected_data['EVENT_3'] = scraped[0] # Edit index to requirement 
        except:
            print("Could not find the element on this page. event: ", event, "\n")
    
    ## FOR EVENTS WITH PARAMETERS 
    elif event == 'EVENT_WITH_PARAMS':   
        print('event is: ', event)
        driver.switch_to.default_content()
        iframes = get_list_of_all_frames_on_page()
        driver.switch_to.frame(iframes[0])
        time.sleep(3)
        # try:
        element_present = WebDriverWait(driver, 1).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//*[@class="value ng-scope layout-row"]')
            )
        )
        html = driver.execute_script('return document.documentElement.innerHTML')
        soup = BeautifulSoup(html, 'html.parser')
        # print(soup.text[:500], "\n")
        print("number of event rows found: ",
              len(soup.findAll('text', {"dominant-baseline": "center"})))
        event_with_params_scraped = []
        if len(soup.findAll('text', {"dominant-baseline": "center"})) != 0:
            contents_of_page = soup.findAll('text', {"dominant-baseline": "center"})
            print("There are this many items to loop through: ", 
                  len(soup.findAll('text', {"dominant-baseline": "center"})))
            for content in range(len(contents_of_page)):
                content = contents_of_page[content]     # set the variable content to be the first item of the list
                content = content.text.strip()
                print(content)
                event_with_params_scraped.append(content)
            print(event_with_params_scraped)
            print("\n")
            if event == 'EVENT_WITH_PARAMS':
                # Filter the collected data to get only what is required
                for data_point in event_with_params_scraped:
                    if '%' in data_point:
                        event_with_params_scraped.remove(data_point)
                # Store that data in global var
                number_of_times_to_loop = (len(event_with_params_scraped))/2
                print("Number of times to loop = ", number_of_times_to_loop)
                for i in range(int(number_of_times_to_loop)):
                    event_param = event_with_params_scraped[:2]
                    print(event_detail)
                    collected_data['EVENT_WITH_PARAMS'].append(event_detail)
                    print('appended')
                    print(collected_data)
                    del event_with_params_scraped[:2]

	else:
        print('Still need to write the scraping code for this event. ')


def get_list_of_all_frames_on_page():
    print("Looking for all iframes")
    iframes = driver.find_elements_by_tag_name("iframe")
    number_of_iframes = len(iframes)
    while number_of_iframes != 5:
        iframes = driver.find_elements_by_tag_name("iframe")
        if len(iframes) == 5:  # This should not be needed... but it doesn't work without it
            break
        else:
            time.sleep(1)
    time.sleep(2)
    iframes = driver.find_elements_by_tag_name("iframe")
    print("Found ", number_of_iframes, " iframes")          
    return iframes


def check_for_logged_activities():
    print('check_for_logged_activities')
    iframes = get_list_of_all_frames_on_page()
    if len(iframes) == 5:  # In the case that there are only 5 frames (expected case)
        driver.switch_to.frame(iframes[0])
        try:
            element_present = WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.XPATH, '//*[@class="no-data-title ng-binding"]')))
            print("found no-data element. ")
        except:
            print("Could not find no-data element on all events page. ")
            element_present = False
        return (element_present)

    else:
        print("NOT 5 FRAMES ON ALL EVENTS PAGE")

    driver.switch_to.default_content()


def store_in_spreadsheet(collected_data):
    
    wb = openpyxl.load_workbook('test_sheet.xlsx',  # filename here 
                                data_only=True)
    sheet = wb.get_sheet_by_name('Sheet1')          # sheet name here

    row = sheet.max_row
    for i in collected_data:
        # Date col. added against user / set of events 
        if i == 'date':
            cell = sheet['A' + str(row+1)]
            cell.value = collected_data['date']

        elif i == 'EVENT_1':
            cell = sheet['B' + str(row+1)]
            cell.value = collected_data['EVENT_1']

        elif i == 'EVENT_2':
            cell = sheet['C' + str(row+1)]
            cell.value = collected_data['EVENT_2']

        elif i == 'EVENT_3':
            cell = sheet['D' + str(row+1)]
            cell.value = collected_data['EVENT_3']

        # For some events, we stored arrays, tuples, or JSON-like structures
        elif i == 'EVENT_WITH_PARAMS':
            print(len(collected_data['EVENT_WITH_PARAMS']))
            cell = sheet['E' + str(row + 1)]
            event_name_and_time = ''
            # content = ''
            for event_list in collected_data['EVENT_WITH_PARAMS']:
                print(event_list)
                content = ''
                for item_in_event_list in event_list:
                    print(item_in_event_list)
                    content = content + item_in_event_list + ' '
                event_name_and_time = event_name_and_time + content
                print(event_name_and_time)
            if len(event_name_and_time) > 0:
                cell.value = event_name_and_time

    wb.save(filename='test_sheet.xlsx')
    print('saved')


def get_yesterdays_date():
    today = datetime.datetime.now()
    yesterday_str = str(today)[:10]
    return yesterday_str


