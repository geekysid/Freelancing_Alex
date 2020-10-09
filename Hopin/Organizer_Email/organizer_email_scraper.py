#!/user/local/bin/python3 -W ignore::DeprecationWarning


########################################
#                                      #
#        SCRAPER FOR HOPI - EMAIL      #
#           By: SIDDHANT SHAH          #
#             Dt: 09-10-2020           #
#     siddhant.shah.1986@gmail.com     #
#   **Just for Educational Purpose**   #
#                                      #
########################################

# important imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from termcolor import cprint
from datetime import datetime
import pandas as pd
import json, time, os, csv, pyfiglet


# global variables
BROWSER = None       # Browser Instance
EVENTS = []          # list of all persons
WAIT_TIME = 10       # Time to wait for ndes to be loaded


def intro_deco():
    print()
    print(pyfiglet.figlet_format(' GeekySid'))
    print()
    print(" ", '#'*40)
    print(" ", "#        SCRAPER FOR HOPI - EMAIL      #")
    print(" ", "#           By: SIDDHANT SHAH          #")
    print(" ", "#             Dt: 09-10-2020           #")
    print(" ", "#     siddhant.shah.1986@gmail.com     #")
    print(" ", "#   **Just for Educational Purpose**   #")
    print(" ", '#'*40)
    print()


# starting an instance of browser
def get_browser_instance(headless=True):
    global BROWSER

    chrome_options = Options()
    chrome_options.headless = headless

    # Starting web browser
    CHROME_DRIVER_PATH = '/home/siddhant/Documents/Freelancing/chromedriver'
    BROWSER = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=chrome_options)
    BROWSER.get('https://hopin.to/sign_in')
    login()


# pulling login credentials from JSON file
def get_login_cred():
    cred_dir = os.getcwd().rsplit('/', 1)[0].rsplit('/', 1)[0]
    login_cred_file = f'{cred_dir}/login_creds.json'

    if os.path.exists(login_cred_file):
        with open(login_cred_file, 'r') as cred:
            return json.load(cred)['hopin']
    else:
        return None


# login into the website
def login():
    creds = get_login_cred()
    if creds:
        cprint(f'\n  [+] Logging into the Website', 'blue', attrs=['bold'])
        # username_field = WebDriverWait(BROWSER, WAIT_TIME).until(EC.visibility_of_element_located((By.ID, 'user_email')))
        # password_field = WebDriverWait(BROWSER, WAIT_TIME).until(EC.visibility_of_element_located((By.ID, 'user_password')))
        # login_button_xpath = '//*[@id="new_user"]/input[2]'

        # username_field.send_keys(creds['username'])
        # time.sleep(0.5)
        # password_field.send_keys(creds['password'])
        # time.sleep(0.5)
        # BROWSER.find_element_by_xpath(login_button_xpath).click()

        time.sleep(3)

        cprint(f'\n  [+] Going to  the Events Page', 'blue', attrs=['bold'])
        # event_xpath = '/html/body/div[2]/div[2]/div[1]/div/a[2]'
        # WebDriverWait(BROWSER, WAIT_TIME).until(EC.visibility_of_element_located((By.XPATH, event_xpath)))
        BROWSER.get('https://hopin.to/events')
        events_page()

    else:
        print('NO LOGIN CREDS')


# applying date and keyword filter
def apply_filters():
    cprint(f'\n  [+] Applying Filters', 'blue', attrs=['bold'])

    if os.path.exists('filter.json'):
        with open('filter.json', 'r') as file:
            filter_ = json.load(file)

        keyword_filter = filter_['keyword'] and not filter_['keyword'] == ''
        date_filter = filter_['date'] and not filter_['date'] == ''

        if keyword_filter:
            keyword_field_xpath = '/html/body/div[2]/div/div[1]/div/form/input[1]'
            WebDriverWait(BROWSER, WAIT_TIME).until(EC.visibility_of_element_located((By.XPATH, keyword_field_xpath))).send_keys(filter_['keyword'])
            cprint(f'      [>] Keyword Filter: {filter_["keyword"]}', 'cyan')

        if date_filter:
            date_field_xpath = '/html/body/div[2]/div/div[1]/div/form/div/input'
            WebDriverWait(BROWSER, WAIT_TIME).until(EC.visibility_of_element_located((By.XPATH, date_field_xpath))).send_keys(filter_['date'])
            cprint(f'      [>] Date Filter: {filter_["date"]}', 'cyan')

        if keyword_filter or date_filter:
            butn_field_xpath = '/html/body/div[2]/div/div[1]/div/form/button'
            WebDriverWait(BROWSER, WAIT_TIME).until(EC.visibility_of_element_located((By.XPATH, butn_field_xpath))).click()
            cprint(f'      [>] Filters applied!!', 'cyan')
        else:
            cprint(f'      [>] No Filters to be applied', 'cyan')
    else:
        pass


# loading all events on the page
def load_all_events():
    cprint(f'\n  [+] Loading All Events', 'blue', attrs=['bold'])
    load_btn_id = 'load-more-events'
    click_counter = 1

    while True:
        try:
            # clicking on load button
            load_more_element = WebDriverWait(BROWSER, WAIT_TIME).until(EC.visibility_of_element_located((By.ID, load_btn_id)))
            time.sleep(1)
            load_more_element.send_keys(Keys.CONTROL + Keys.END)
            load_more_element.click()
            cprint(f'      [>] Cicked Load More button {click_counter} times', 'cyan')

            # ending loading more events after certain number of click
            if click_counter == 5:
                break

            time.sleep(3)
            click_counter += 1
        except Exception as e:
            print(str(e))
            cprint(f'      [>] All Events Loaded!!', 'cyan')
            break


# fetching all required data for events
def fetching_event_data(link_list):
    for link in link_list:
        BROWSER.get(link)
        time.sleep(2.5)

        # event name
        try:
            event_name_xpath = '/html/body/div[2]/div[1]/div[1]/h1'
            event_name = BROWSER.find_element_by_xpath(event_name_xpath).text.strip()
            cprint(f'\n      [>] Event: {event_name}', 'cyan')
        except:
            event_name = None

        # event start time
        try:
            start_time_xpath = '/html/body/div[2]/div[1]/div[1]/div[1]/div[1]/span[2]/strong[1]/time'
            timeZone_xpath = '/html/body/div[2]/div[1]/div[1]/div[1]/div[1]/span[2]/time'
            start_time = BROWSER.find_element_by_xpath(start_time_xpath).text.strip()
            timeZone = BROWSER.find_element_by_xpath(timeZone_xpath).text.strip()
            start_time = f'{start_time} {timeZone}'
            cprint(f'          [>>] Start Time: {start_time}', 'yellow')
        except:
            start_time = None

        # event end time
        try:
            end_time_xpath = '/html/body/div[2]/div[1]/div[1]/div[1]/div[1]/span[2]/strong[2]/time'
            timeZone_xpath = '/html/body/div[2]/div[1]/div[1]/div[1]/div[1]/span[2]/time'
            end_time = BROWSER.find_element_by_xpath(end_time_xpath).text.strip()
            timeZone = BROWSER.find_element_by_xpath(timeZone_xpath).text.strip()
            start_time = f'{start_time} {timeZone}'
            cprint(f'          [>>] End Time: {end_time}', 'yellow')
        except:
            end_time = None

        # number of people attending
        try:
            attendee_count_xpath = '/html/body/div[2]/div[1]/div[1]/div[1]/div[2]/span[2]/strong'
            attendee_count = BROWSER.find_element_by_class_name(attendee_count_xpath).text.strip()
            cprint(f'          [>>] Attendee Count: {attendee_count}', 'yellow')
        except:
            attendee_count = None

        # event description
        try:
            description_class_name = 'rich-text'
            description = BROWSER.find_element_by_class_name(description_class_name).text.strip()
            cprint(f'          [>>] Description: {description[:20]}...', 'yellow')
        except:
            description = None

        # organiser Data
        try:
            organisers_main_div_xpath = '/html/body/div[2]/div[1]/div[3]/div[2]'
            organiser_main_div = BROWSER.find_element_by_xpath(organisers_main_div_xpath)
            organiser_name = organiser_main_div.find_element_by_tag_name('h2').text.strip()
            cprint(f'          [>>] Organiser: {organiser_name}', 'yellow')
        except Exception as e:
            print(str(e))
            organiser_name = None

        # organiser Email
        try:
            link_elements = organiser_main_div.find_elements_by_tag_name('a')
            for link_element in link_elements:
                link = link_element.get_attribute('href')
                if link[:7] == 'mailto:':
                    mail = link[7:]
                    cprint(f'          [>>] Mail Address: {mail}', 'yellow')
        except:
            mail = None

        EVENTS.append({
            'name': event_name,
            'url': BROWSER.current_url,
            'start_time': start_time,
            'end_time': end_time,
            'attendees': attendee_count,
            'description': description,
            'organiser': organiser_name,
            'email': mail
        })

    # saving fetched data to the csv
    save_to_csv()


# pulling events by for the page
def pulling_events_data():
    events = BROWSER.find_elements_by_class_name('card')
    link_list = []
    for event in events:
        link_list.append(event.get_attribute('href'))

    fetching_event_data(link_list)


# function that does
def events_page():
    apply_filters()

    page_counter = 1
    more_events_available = True

    # looping through pages
    while more_events_available:
        try:
            # getting url of next page
            load_more_btn = WebDriverWait(BROWSER, WAIT_TIME).until(EC.visibility_of_element_located((By.ID, 'load-more-events')))
            url = load_more_btn.get_attribute('href')
        except:
            more_events_available = False

        # getting events for current page
        cprint(f'\n  [>] Getting Events from Page # {page_counter}', 'blue', attrs=['bold'])
        pulling_events_data()

        # only if more events are available
        if more_events_available:
            BROWSER.get(url)
            page_counter += 1

    # load_all_events()
    events = BROWSER.find_elements_by_class_name('card')
    print(len(events))
    input()


# saving file to csv
def save_to_csv():
    df = pd.DataFrame(EVENTS)
    # df = df.transpose()
    df.to_csv('hopin.csv', index=False)


# function which initiates the program
def main():
    intro_deco()
    get_browser_instance()  # instantiating browser instance
    get_people_loop()       # functo to load all people on page

    BROWSER.quit()


# logging time into a csv file
def time_logger(time_dict):
    time_df = pd.DataFrame(time_dict, columns=['start_time', 'end_time', 'execution_time'])
    try:
        if os.path.exists('time_log.csv'):
            time_df = pd.concat([pd.read_csv('time_log.csv'), time_df])
    except:
        pass

    time_df.to_csv('time_log.csv', index=False)


# printing time to console
def timer(start_time, start_time_str):

    end_time = time.time()       # time at which script ends execution
    end_time_str = datetime.now().strftime('%m/%d/%Y, %H:%M:%S')

    # calculating execution time of the script
    execution_time = end_time-start_time
    hrs = int(execution_time//3600)
    mins = int((execution_time%3600)//60)
    secs = int((execution_time%3600)%60)
    execution_time_str = f"{hrs}hrs {mins}mins {secs}secs"

    # logging time to csv
    time_final = [[ start_time_str, end_time_str, execution_time_str ]]
    time_logger(time_final)

    # printing requird data
    print()
    cprint("="*45, "blue", attrs=['bold'])
    cprint(f"  Start Time: {start_time_str}", "blue", attrs=['bold'])
    cprint(f"  End Time  : {end_time_str}", "blue", attrs=['bold'])
    cprint(f"  Total Time: {execution_time_str}", "blue", attrs=['bold'])
    cprint("="*45, "blue", attrs=['bold'])
    print()


if __name__ == '__main__':
    start_time = time.time()     # time at which script starts execution
    start_time_str = datetime.now().strftime('%m/%d/%Y, %H:%M:%S')
    main()                              # Initiating Scrapper
    timer(start_time, start_time_str)   # Printing time log to console
