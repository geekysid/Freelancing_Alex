#!/user/local/bin/python3 -W ignore::DeprecationWarning


########################################
#                                      #
#         SCRAPER FOR EventBrite       #
#           By: SIDDHANT SHAH          #
#             Dt: 07-10-2020           #
#     siddhant.shah.1986@gmail.com     #
#   **Just for Educational Purpose**   #
#                                      #
########################################


# important imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from termcolor import cprint
import time, pyfiglet
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


# global variables
BROWSER = None       # Browser Instance
PEOPLE = []          # list of all persons
SLEEP_TIME = 0.5
WAIT_TIME = 10       # Time to wait for ndes to be loaded


def intro_deco():
    print()
    print(pyfiglet.figlet_format(" GeekySid"))
    print()
    print(' ', '#'*40)
    print(' ', "#                                      #")
    print(' ', "#         SCRAPER FOR EventBrite       #")
    print(' ', "#           By: SIDDHANT SHAH          #")
    print(' ', "#             Dt: 07-10-2020           #")
    print(' ', "#     siddhant.shah.1986@gmail.com     #")
    print(' ', "#   **Just for Educational Purpose**   #")
    print(' ', "#                                      #")
    print(' ', '#'*40)
    print()


# starting an instance of browser
def get_browser_instance(headless=False):
    global BROWSER

    chrome_options = Options()
    chrome_options.headless = headless

    # Starting web browser
    CHROME_DRIVER_PATH = '/home/siddhant/Documents/Freelancing/chromedriver'
    BROWSER = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=chrome_options)
    BROWSER.get('https://www.eventbrite.com/signin/')
    login()


# loging into website
def login():
    cprint(f'\n  [+] Logging into the Website', 'blue', attrs=['bold'])
    time.sleep(2)
    # entering email in username field
    username_field = WebDriverWait(BROWSER, WAIT_TIME).until(EC.visibility_of_element_located((By.ID, 'email')))
    username_field.send_keys('siddhant.dummy@gmail.com')

    # clicking on continue button
    continue_button_xpath = '/html/body/div[1]/div/div[2]/div/div/div/div[1]/div/main/div/div/div/div[2]/form/div[2]/button'
    continue_button = BROWSER.find_element_by_xpath(continue_button_xpath).click()
    time.sleep(1)

    # entering password
    password_field = WebDriverWait(BROWSER, WAIT_TIME).until(EC.visibility_of_element_located((By.ID, 'password')))
    password_field.send_keys('Siddhant@123')
    time.sleep(2)

    # clicking on login button
    login_button_xpath = '//*[@id="root"]/div/div[2]/div/div/div/div[1]/div/main/div/div/div/div[2]/form/div[3]/button'
    login_button = BROWSER.find_element_by_xpath(login_button_xpath).click()
    time.sleep(2)
    BROWSER.get('https://www.eventbrite.com/d/online/free--conferences/conference/')
    start_pulling_events()


# function that loope through pages and pull events
def start_pulling_events():
    page_count_xpath = '/html/body/div/div/div[2]/div/div/div/div[1]/div/main/div/div/section[1]/footer/div[1]/div/ul/li[2]'
    page_count = WebDriverWait(BROWSER, WAIT_TIME).until(EC.visibility_of_element_located((By.XPATH, page_count_xpath)))
    total_pages = int(page_count.text.split()[2].strip())

    for i in range(total_pages):
        cprint(f'\n  [+] EVENTS Page # {i+1}', 'blue', attrs=['bold'])
        BROWSER.get(f'https://www.eventbrite.com/d/online/free--conferences/conference/?page={i+1}')
        fetching_free_events()


# puling events from page
def fetching_free_events():
    event_list_class = 'ul.search-main-content__events-list'
    event_list = WebDriverWait(BROWSER, WAIT_TIME).until(EC.visibility_of_element_located((By.CSS_SELECTOR, event_list_class)))

    event_list = event_list.find_elements_by_tag_name('li')

    for event in event_list:
        element = event.find_elements_by_tag_name('a')[1]

        event_type_class = 'eds-event-card-content__sub-content'
        event_type_element = event.find_elements_by_class_name(event_type_class)[0]

        if event_type_element.text.strip() == 'Free':
            cprint(f'\n      [>] Event: {element.text}', 'cyan')
            event_page(element.get_attribute('href'))
        else:
            continue


# opening event page in new tab
def event_page(event_url):
    # save main_window
    main_window = BROWSER.current_window_handle

    # open new blank tab
    BROWSER.execute_script("window.open();")

    # switch to the new window which is second in window_handles array
    new_tab = BROWSER.window_handles[1]
    BROWSER.switch_to_window(new_tab)

    # open successfully and close
    BROWSER.get(event_url)
    time.sleep(2)

    # getting event id from url
    event_id = BROWSER.current_url.split('?')[0].rsplit('-')[-1]
    register_button_id = f'eventbrite-widget-modal-trigger-{event_id}'
    cprint(f'          [>>] Clicked to Register', 'yellow')
    WebDriverWait(BROWSER, WAIT_TIME).until(EC.visibility_of_element_located((By.ID, register_button_id))).click()
    register_for_event(event_id)

    BROWSER.close()

    # back to the main window
    BROWSER.switch_to_window(main_window)


# function that register us for events
def register_for_event(event_id):
    time.sleep(5)


    iframe_id = f'eventbrite-widget-modal-{event_id}'
    BROWSER.switch_to.frame(iframe_id)
    button = BROWSER.find_elements_by_tag_name('button')[0]
    cprint(f'          [>>] Heading for Checkout', 'yellow')
    button.click()

    checkout()


# function to checkout
def checkout():
    WebDriverWait(BROWSER, WAIT_TIME).until(EC.visibility_of_element_located((By.ID, 'buyer.N-first_name')))

    try:
        input_fields = BROWSER.find_elements_by_xpath('//*[contains(@id, "N-first_name")]')
        for input_field in input_fields:
            try:
                input_field.send_keys('Siddhant')
            except:
                pass
    except:
        pass

    try:
        input_fields = BROWSER.find_elements_by_xpath('//*[contains(@id, "N-last_name")]')
        for input_field in input_fields:
            try:
                input_field.send_keys('Shah')
            except:
                pass
    except Exception as e:
        pass

    try:
        input_fields = BROWSER.find_elements_by_xpath('//*[contains(@id, "N-email")]')
        for input_field in input_fields:
            try:
                input_field.send_keys('siddhant.dummy@gmail.com')
            except:
                pass
    except:
        pass

    try:
        BROWSER.find_element_by_id('buyer.confirmEmailAddress').send_keys('siddhant.dummy@gmail.com')
    except:
        pass

    try:
        BROWSER.find_element_by_id('buyer.N-cell_phone').send_keys('8584852092')
    except:
        pass

    try:
        BROWSER.find_element_by_id('N-homeaddress1').send_keys('Kankurgachi')
    except:
        pass
    try:
        BROWSER.find_element_by_id('N-homecity').send_keys('Kolkata')
    except:
        pass
    try:
        BROWSER.find_element_by_id('N-homepostal').send_keys('700054')
    except:
        pass
    try:
        BROWSER.find_element_by_id('N-homecountry').send_keys('india')
    except:
        pass
    try:
        BROWSER.find_elements_by_xpath('//*[contains(@id, "N-job_title")]').send_keys('CA') # JOB
    except:
        pass
    try:
        BROWSER.find_elements_by_xpath('//*[contains(@id, "N-company")]').send_keys('SIDDHANT') # company
    except:
        pass
    try:
        BROWSER.find_elements_by_xpath('//*[contains(@id, "U-35498227")]').send_keys('other') # affiliation (type OTHER)
    except:
        pass
    try:
        BROWSER.find_elements_by_xpath('//*[contains(@id, "U-35498229-1")]').click() # standard Alumn
    except:
        pass

    time.sleep(2)
    button_xpath = '//*[@id="root"]/div/div/div/div[1]/div[1]/div/main/div/div[2]/div/nav/div/button'
    cprint(f'          [>>] Waiting for Confirmation', 'yellow')
    BROWSER.find_element_by_xpath(button_xpath).click()

    success_el = WebDriverWait(BROWSER, WAIT_TIME).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.follow-layout__thank-you-message-text-container')))
    message = success_el.find_element_by_tag_name('h3').text.strip()
    if message == 'Thanks for your order!':
        cprint(f'          [>>] Registered', 'green', attrs=['bold'])

    time.sleep(2)



if __name__ == '__main__':
    intro_deco()
    get_browser_instance()  # instantiating browser instance
    BROWSER.quit()
