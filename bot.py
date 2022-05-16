from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import info, time

def connect(keyword, till_page):
    for page in range(1, till_page +1):
        print("Checking on page %s" % (page))
        queryurl = "https://www.linkedin.com/search/results/people/?keywords="+ keyword +"&origin=SWITCH_SEARCH_VERTICAL&page="+ str(page) +"&sid=oW3"
        driver.get(queryurl)
        time.sleep(3)
        driver.find_element_by_tag_name('html').send_keys(Keys.END)
        time.sleep(3)
        linkedin_urls = driver.find_elements_by_class_name("reusable-search__result-container")
        print("PAGE %s: %s connections" % (page, len(linkedin_urls)))
        for index, result in enumerate(linkedin_urls, start=1):
            text = result.text.split("\n")[0]
            connection_action = result.find_elements_by_class_name("artdeco-button__text")
            if connection_action:
                connection = connection_action[0]
            else:
                print("%s ) CANT: %s" % (index, text))
                continue
            
            if connection.text == "Connect":
                try:
                    coordinates = connection.location_once_scrolled_into_view
                    driver.execute_script("window.scrollTo(%s, %s);" % (coordinates["x"], coordinates["y"]))
                    time.sleep(3)
                    connection.click()
                    time.sleep(3)
                    if driver.find_element_by_class_name("artdeco-button--primary").is_enabled():
                        driver.find_element_by_class_name("artdeco-button--primary").click()
                        time.sleep(3)
                        print("%s ) SENT: %s" % (index, text))
                    else:
                        driver.find_element_by_class_name("artdeco-modal__dismiss")[0].click()
                        print("%s ) Cant connect: %s" % (index, text))
                except Exception as e:
                    print("%s ) ERROR: %s - %s" % (index, text, e))
                time.sleep(3)
            elif connection.text == "Pending":
                print("%s ) Pending: %s" % (index, text))
            else:
                if text : print("%s ) None: %s" % (index, text))
                else : print("%s ) ERROR: Limit Maybe Reached" % (index))
                    
                            


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
print("Web driver initiated.")

driver.get('https://www.linkedin.com/login')
time.sleep(3)
driver.find_element(By.ID, "username").send_keys(info.username)
driver.find_element(By.ID, 'password').send_keys(info.password)
driver.find_element(By.XPATH, ('//*[@type="submit"]')).click()
time.sleep(3)

connect(info.keyword, info.till_page)

driver.quit()

