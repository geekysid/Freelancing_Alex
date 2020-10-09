#!/user/local/bin/python3 -W ignore::DeprecationWarning


########################################
#                                      #
#   SCRAPER FOR HOPI - ATTENDEE DATA   #
#           By: SIDDHANT SHAH          #
#             Dt: 08-10-2020           #
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
from selenium.webdriver.common.action_chains import ActionChains
from termcolor import cprint
from datetime import datetime
import pandas as pd
import json, time, os, csv, pyfiglet


# global variables
BROWSER = None       # Browser Instance
PEOPLE = []          # list of all persons
SLEEP_TIME = 0.5
WAIT_TIME = 600       # Time to wait for ndes to be loaded


def intro_deco():
    print()
    print(pyfiglet.figlet_format(' GeekySid'))
    print()
    print(" ", '#'*40)
    print(" ", "#   SCRAPER FOR HOPI - ATTENDEE DATA   #")
    print(" ", "#           By: SIDDHANT SHAH          #")
    print(" ", "#             Dt: 08-10-2020           #")
    print(" ", "#     siddhant.shah.1986@gmail.com     #")
    print(" ", "#   **Just for Educational Purpose**   #")
    print(" ", '#'*40)
    print()


# starting an instance of browser
def get_browser_instance(headless=False):
    global BROWSER

    chrome_options = Options()
    chrome_options.headless = headless

    # Starting web browser
    CHROME_DRIVER_PATH = '/home/siddhant/Documents/Freelancing/chromedriver'
    BROWSER = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=chrome_options)
    BROWSER.get('https://hopin.to/events/')


# saving file to csv
def save_to_csv():
    df = pd.DataFrame(PEOPLE)
    # df = df.transpose()
    df.to_csv('hopin.csv', index=False)


# function that goes to each model url fetched from fetch_iphone_models()
def load_all_people():
    click_count = 0
    while True:
        try:
            click_count += 1
            loadMore_xpath = f'//*[@id="__next"]/div[1]/div[6]/aside/div[2]/div[3]/div/div[2]/div/div[2]/div[3]/div[{(click_count*10)+1}]'
            WebDriverWait(BROWSER, WAIT_TIME).until(EC.visibility_of_element_located((By.XPATH, loadMore_xpath))).click()
            # loadMore_class = 'div.people-list_load-more__2dx_z'
            # WebDriverWait(BROWSER, WAIT_TIME).until(EC.visibility_of_element_located((By.CSS_SELECTOR, loadMore_class))).click()
            cprint(f"  [>] {10} more People loaded ({click_count*10})", "green")

            # if click_count == 10:
            #     break

        except Exception as e:
            # input('EXCEPTION: ' + str(e))
            break


# function to fetch data of person
def get_person_data():
    temp_dict = {}
    # name
    try:
        name_xpath = '/html/body/div/div[1]/div[6]/aside/div[2]/div[3]/div/div/div[1]/div/section[1]/div/div[1]'
        temp_dict['name'] = BROWSER.find_element_by_xpath(name_xpath).text.strip()
        cprint(f"      [>] Name: {temp_dict['name']}", 'yellow')
    except:
        temp_dict['name'] = None

    # designation
    try:
        designation_xpath = '/html/body/div/div[1]/div[6]/aside/div[2]/div[3]/div/div/div[1]/div/section[1]/div/div[2]'
        temp_dict['designation'] = BROWSER.find_element_by_xpath(designation_xpath).text.strip()
        cprint(f"      [>] Designation: {temp_dict['designation']}", 'cyan')
    except:
        temp_dict['designation'] = None

    # about
    try:
        # clicking show more
        try:
            show_more_xpath = '/html/body/div/div[1]/div[6]/aside/div[2]/div[3]/div/div/div[1]/div/section[3]/div/button'
            show_more_btn = BROWSER.find_element_by_xpath(show_more_xpath)
            if show_more_btn.text.strip() == 'Show More':
                show_more_btn.click()
        except:
            pass
        temp_dict['about'] = BROWSER.find_element_by_class_name('test-id-about').text.strip()
        cprint(f"      [>] About: {temp_dict['about']}", 'cyan')
    except:
        temp_dict['about'] = None

    # social links
    try:
        social_link = {}
        socials = BROWSER.find_element_by_class_name('profile-header_social__19aBC').find_elements_by_tag_name('a')

        for social in socials:
            platform = social.get_attribute('class').split('-')[-1]
            link = social.get_attribute('href')
            temp_dict[platform] = link
            cprint(f"      [>] {platform}: {link}", 'cyan')
    except Exception as e:
        pass

    return temp_dict


# fetching configration data for clickable HTML layout
def get_people_loop():
    global PEOPLE
    cprint(f"\n  [>] Going to People Tab", "cyan")

    # clicking on People's tab
    peopleTab_xpath = '/html/body/div/div[1]/div[6]/aside/div[1]/div/div/button[3]'
    WebDriverWait(BROWSER, WAIT_TIME).until(EC.visibility_of_element_located((By.XPATH, peopleTab_xpath))).click()

    # waiting for people's tab t be loaded with data
    people_div_xpath = '/html/body/div/div[1]/div[6]/aside/div[2]/div[3]/div/div[2]/div/div[2]'
    WebDriverWait(BROWSER, WAIT_TIME).until(EC.visibility_of_element_located((By.XPATH, people_div_xpath)))

    # getting all loaded people elements
    people_div_xpath = '/html/body/div/div[1]/div[6]/aside/div[2]/div[3]/div/div[2]/div/div[2]/div[1]/div'
    people_counter = 366

    # looping through all loaded people elements
    while True:
        try:
            person = BROWSER.find_element_by_xpath(f'{people_div_xpath}[{people_counter}]')

            # focus person
            actions = ActionChains(BROWSER)
            actions.move_to_element(person).perform()

            # clicking on people to get its info
            person.find_element_by_tag_name('div').click()

            # waiting for people info to be loaded
            WebDriverWait(BROWSER, WAIT_TIME).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div[1]/div[6]/aside/div[2]/div[3]/div/div/div[1]/div/section[1]/div/div[1]')))
            PEOPLE.append(get_person_data())
            people_counter += 1

            # saving data to csv after every 10th person
            if people_counter % 10 == 0:
                save_to_csv()

            # clicking on back arrow to go back to all people
            BROWSER.find_element_by_class_name('profile-header_back__q25eA').click()
            time.sleep(SLEEP_TIME)
            print()

        except Exception as e:
            save_to_csv()
            people_counter = 1
            try:
                people_div_xpath = '/html/body/div/div[1]/div[6]/aside/div[2]/div[3]/div/div[2]/div/div[2]/div[3]/div'
                time.sleep(2)
                load_all_people()
            except Exception as e:
                # input(str(e))
                pass
            # pass

    save_to_csv()


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
