# Firebase_scraper_clean        #
# Version_1.2                   #


### IMPORT REQUIRED LIBRARIES 
import time
import firebase_web_scraper_src


### LAUNCH BROWSER 
try:
    driver = webdriver.Chrome("/usr/local/bin/chromedriver")  
except:
    print("Could not launch chrome. Check path for chromedriver on your device.")
    quit()
    # TODO - send me an email if this occurs.


### INITIALIZE GLOBAL VARIABLES 
event_page_urls = {
    'event_1': 'https://console.firebase.google.com/project/',
    'event_2': 'https://console.firebase.google.com/project/',
    'event_3': 'https://console.firebase.google.com/project/',
    'all_events': 'https://console.firebase.google.com/project/',
}

all_users_collected_data = []   


### MAIN LOOP 
start = time.time()

open_browser_to_firebse()
sign_in_to_firebase()

list_of_users = get_list_of_users()           

for i in range(len(list_of_users)):

    user_id = str(list_of_users[i])

    collected_data = {} # clear single user's collected data

    access_events_page_for_user(user_id)
    if check_for_logged_activities() == False:
        logged_events = get_logged_events()
        check_if_logged_events_are_required(logged_events, user_id)
        collected_data['user_id'] = user_id
        collected_data['date'] = get_yesterdays_date()
        store_in_spreadsheet(collected_data)
    else:
        print('No logged activities for this user: ', user_id, "\n")

    if len(collected_data) != 0:
        store_in_spreadsheet(collected_data)
        all_users_collected_data.append(collected_data)

# print(all_users_collected_data)

end = time.time()
print("\n", end - start)

