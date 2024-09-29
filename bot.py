from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import random

class botClass():

    def __init__(self, id):
        self.runID = id

        self.driver = webdriver.Chrome(options=self.browser_options())
        self.driver.get("https://www.linkedin.com/login")
        self.locator = {
            "next": (By.CSS_SELECTOR, "button[aria-label='Continue to next step']"),
            "review": (By.CSS_SELECTOR, "button[aria-label='Review your application']"),
            "submit": (By.CSS_SELECTOR, "button[aria-label='Submit application']"),
            "error": (By.CLASS_NAME, "artdeco-inline-feedback__message"),
            "upload_resume": (By.XPATH, "//*[contains(@id, 'jobs-document-upload-file-input-upload-resume')]"),
            "upload_cv": (By.XPATH, "//*[contains(@id, 'jobs-document-upload-file-input-upload-cover-letter')]"),
            "follow": (By.CSS_SELECTOR, "label[for='follow-company-checkbox']"),
            "upload": (By.NAME, "file"),
            "search": (By.CLASS_NAME, "jobs-search-results-list"),
            "links": ("xpath", '//div[@data-job-id]'),
            "fields": (By.CLASS_NAME, "jobs-easy-apply-form-section__grouping"),
            "radio_select": (By.CSS_SELECTOR, "input[type='radio']"),
            "multi_select": (By.XPATH, "//*[contains(@id, 'text-entity-list-form-component')]"),
            "text_select": (By.CLASS_NAME, "artdeco-text-input--input"),
            "2fa_oneClick": (By.ID, 'reset-password-submit-button'),
            "easy_apply_button": (By.XPATH, '//button[contains(@class, "jobs-apply-button")]')
        }
        self.jobIDs = []
 
    def browser_options(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")

        return options

    def login(self):

        time.sleep(2)
        self.elem = self.driver.find_element(By.ID, "username")
        self.elem.send_keys("s64053094@gmail.com")
        time.sleep(1)
        self.elem = self.driver.find_element(By.ID, "password")
        self.elem.send_keys("Googleearth123!")
        self.elem = self.driver.find_element("xpath",'//*[@id="organic-div"]/form/div[3]/button')
        time.sleep(1)
        self.elem.click()
        time.sleep(5)

        return "logged in"
    
    def findAppPage(self, position, location):

        time.sleep(1)
        self.driver.get("https://www.linkedin.com/jobs/search/?f_LF=f_AL&keywords=" + position + location + "&start=" + "0" + "")
        self.driver.set_window_position(1, 1)
        self.driver.maximize_window()
        time.sleep(5)

        return "logged in"
    
    def scroll(self):
        time.sleep(5)

        try:
            scroll_container = self.driver.find_element(By.CLASS_NAME, "jobs-search-results-list")

            # Scroll within the container to load more results
            for i in range(300, 3800, 100):
                self.driver.execute_script("arguments[0].scrollTo(0, arguments[1]);", scroll_container, i)
                time.sleep(0.1)  # Small delay to ensure new content loads
            
            scroll_container = self.driver.find_element(By.CLASS_NAME, "jobs-search-results-list")

            
            links = self.driver.find_elements("xpath", '//div[@data-job-id]')

            for i in links:
                if "Easy Apply" in i:
                    self.jobIDs.append(i.get_attribute("data-job-id"))

        except Exception as e:
            log.error(f"An error occurred during scrolling: {e}")

        time.sleep(500)

    def applyLoop(self, job_id):
        for x in job_id:
            self.driver.get(f"https://www.linkedin.com/jobs/view/{x}/")

    
    def nextPage(self):

        time.sleep(3)
        
        try:
            element = self.driver.find_element("xpath", '//*[@id="ember307"]/span')

        except NoSuchElementException:
            self.applyLoop()
        

random_number = random.randint(1000000000, 9999999999)
my_instance = botClass(random_number)
my_instance.login()
my_instance.findAppPage("full stack", "san diego")
my_instance.scroll()
my_instance.nextPage()


