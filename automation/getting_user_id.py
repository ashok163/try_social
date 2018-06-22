from selenium import webdriver

# from selenium.webdriver.chrome.options import Options

import os

import pickle

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.chrome.options import Options as ChromeOptions

chrome_bin = os.environ.get('GOOGLE_CHROME_SHIM', None)
opts = ChromeOptions()
opts.binary_location = chrome_bin
driver = webdriver.Chrome(chrome_options=opts)

# chrome_options = Options()

# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--window-size=1920x1080")
# chrome_driver = os.getcwd() + "/chromedriver"

# # go to Google and click the I'm Feeling Lucky button
# driver = webdriver.Chrome(chrome_options=chrome_options,
#                           executable_path=chrome_driver)


def used_id_from_username(insta_user_name, username, password):
    username = username
    password = password

    driver.get("https://www.instagram.com")
    driver.implicitly_wait(20)
    pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
    driver.implicitly_wait(10)

    # driver.get("https://www.instagram.com/accounts/login/")
    #
    # cookies = pickle.load(open("cookies.pkl", "rb"))
    # for cookie in cookies:
    #     driver.add_cookie(cookie)
    #
    # driver.implicitly_wait(10)
    #
    #
    # driver.find_element_by_xpath("//input[@name='username']").send_keys(username)
    # driver.find_element_by_xpath("//input[@name='password']").send_keys(password)
    # driver.find_element_by_xpath("//button[contains(.,'Log in')]").click()
    #
    # driver.implicitly_wait(20)

    # cookies = pickle.load(open("cookies.pkl", "rb"))
    # for cookie in cookies:
    #     driver.add_cookie(cookie)

    # driver.implicitly_wait(20)
    url = 'https://www.instagram.com/' + insta_user_name
    driver.get(url)
    driver.implicitly_wait(200)
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

    driver.implicitly_wait(20)

    user_id = driver.execute_script('return window._sharedData.entry_data.ProfilePage[0].graphql.user.id;');

    return user_id;


if __name__ == "__main__":
    pass
