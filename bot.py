from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import random
import logging
import yaml


class botClass():

    def __init__(self):

        with open('addyourinformation.yaml', 'r') as file:
            self.config = yaml.safe_load(file)

        self.driver = webdriver.Chrome(options=self.browser_options())
        self.driver.get("https://www.linkedin.com/login")
        self.jobIDs = []
        self.positions = self.config['positions']
        self.locations = self.config['locations']
        self.mobileNumber = self.config['user_credentials']['mobilenumber']
        self.pageNumber = 0
 
    def browser_options(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")

        return options
    
    def choosePositionLocation(self) -> None:
    
        random_numberP = random.randint(0, 3)
        random_numberL = random.randint(0, 13)
        self.position = self.positions[random_numberP]
        self.location = self.locations[random_numberL]

    def login(self):

        time.sleep(2)
        self.elem = self.driver.find_element(By.ID, "username")
        self.elem.send_keys(self.config['user_credentials']['email'])
        time.sleep(1)
        self.elem = self.driver.find_element(By.ID, "password")
        self.elem.send_keys(self.config['user_credentials']['password'])
        self.elem = self.driver.find_element("xpath",'//*[@id="organic-div"]/form/div[3]/button')
        time.sleep(1)
        self.elem.click()
        time.sleep(20)

        return "logged in"
    
    def findAppPage(self):
        time.sleep(1)
        self.driver.get("https://www.linkedin.com/jobs/search/?keywords=" + self.position + "&location=" + self.location + "&start=" + str(25 * self.pageNumber) + "&f_AL=true")
        self.driver.set_window_position(1, 1)
        self.driver.maximize_window()
        time.sleep(5)

        return "logged in"
    
    def scroll(self):
        time.sleep(5)

        try:
            scroll_container = self.driver.find_element(By.CLASS_NAME, "jobs-search-results-list")

            for i in range(300, 3800, 100):
                self.driver.execute_script("arguments[0].scrollTo(0, arguments[1]);", scroll_container, i)
                time.sleep(0.1)
            
            scroll_container = self.driver.find_element(By.CLASS_NAME, "jobs-search-results-list")

            
            links = self.driver.find_elements("xpath", '//div[@data-job-id]')

            for i in links:
                if "Easy Apply" in i.text:
                    self.jobIDs.append(i.get_attribute("data-job-id"))

        except Exception as e:
            logging.error(f"An error occurred during scrolling: {e}")

        time.sleep(12)

    def process_questions(self):
        time.sleep(0.5)
        try:
            form = self.driver.find_elements(By.XPATH, "//div[contains(@class,'jobs-easy-apply-form-section__grouping')]")
            
            for field in form:
                question = field.text.lower()
                answer = self.ans_question(question)

                try:
                    checkboxes = field.find_elements(By.XPATH, ".//input[@type='checkbox']")
                    if checkboxes:
                        for checkbox in checkboxes:
                            if not checkbox.is_selected():
                                # Use JavaScript to check the checkbox
                                self.driver.execute_script("arguments[0].click();", checkbox)
                                print(f"Checked a checkbox for question: {question}")

                    radio_buttons = field.find_elements(By.XPATH, ".//input[@type='radio']")
                    if radio_buttons:
                        answer = "yes"
                        for radio in radio_buttons:

                            self.driver.execute_script("arguments[0].click();", radio)
                            print(f"Selected 'Yes' for radio button question: {question}")

                    dropdowns = field.find_elements(By.XPATH, ".//*[contains(@id, 'text-entity-list-form-component')]")
                    if dropdowns:
                        for dropdown in dropdowns:
                            options = dropdown.find_elements(By.TAG_NAME, "option")
                            if options:
                                selected_option = random.choice(options[:2])
                                selected_option.click()
                                break

                    # Handle text inputs and text areas (if applicable)
                    text_inputs = field.find_elements(By.CSS_SELECTOR, "input[type='text'], textarea")
                    if text_inputs:
                        for text_input in text_inputs:
                            if text_input.get_attribute('value').strip():
                                print(f"Field already populated with: {text_input.get_attribute('value')}, skipping it.")
                                continue

                            text_input.send_keys(answer)

                            time.sleep(0.5)

                            text_input.send_keys(Keys.ARROW_DOWN)
                            text_input.send_keys(Keys.ENTER)

                except Exception as e:
                    print(f"Error processing field: {e}")
                    pass

        except Exception as e:
            print(f"Error: {e}")
            return

    def ans_question(self, question):
        question_lower = question.lower()
        answer = None

        for key, value in self.config['questions_and_answers'].items():
            if key.lower() in question_lower:
                answer = value
                logging.info(f"Answering question: {question} with answer: {answer}")
                return answer

        logging.info(f"Not able to answer question automatically: {question}")
        answer = "1"
        time.sleep(5)
        return answer

    def apply(self):

        try:

            apply_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "jobs-apply-button--top-card"))
            )
            apply_button.click()
            time.sleep(1)

            try:

                    susButton = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "jobs-apply-button"))
                    )
                    susButton.click()
                    print("Button clicked!")
            except:
                pass


            time.sleep(1)

            try: 
                self.fill_out_mobile()
                time.sleep(3)
                self.next_ButtonInitial = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Continue to next step']")
                self.next_ButtonInitial.click()
                time.sleep(1)

            except:
                pass

        except TimeoutException:
            return
        
        self.attempts = 0
        while (True):
            if (self.attempts > 8):
                break

            self.attempts += 1

            try:
                self.next_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Continue to next step']")
                
                if self.next_button.is_displayed():
                    print("Clicking 'Continue to next step'")
                    time.sleep(3)
                    self.process_questions()
                    self.next_button.click()
                    continue

            except NoSuchElementException:
                print("'Continue to next step' button not found")

            try:
                self.review_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Review your application']")
                if self.review_button.is_displayed():
                    print("Clicking 'Review your application'")
                    self.process_questions()
                    self.review_button.click()
                    time.sleep(3)
                    continue

            except NoSuchElementException:
                print("'Review your application' button not found")

            try:
                self.submit_container = self.driver.find_element(By.CLASS_NAME, "artdeco-modal__content")
                for i in range(300, 1000, 100):
                    self.driver.execute_script("arguments[0].scrollTo(0, arguments[1]);", self.submit_container, i)
                    time.sleep(0.1)
            

                self.follow_button = self.driver.find_element(By.CSS_SELECTOR, "label[for='follow-company-checkbox']")
                if self.follow_button.is_displayed():
                    self.follow_button.click()
                    print("Clicked follow company checkbox")

                self.submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Submit application']")
                if self.submit_button.is_displayed():
                    self.submit_button.click()
                    print("Application submitted")
                    break

            except NoSuchElementException as e:
                print("Submit button or follow checkbox not found:", e)
                break

    def applyLoop(self):
        for x in self.jobIDs:
            self.driver.get(f"https://www.linkedin.com/jobs/view/{x}/")
            self.apply()
            time.sleep(6)
        print('resetting and finding new page')
        time.sleep(1)
        my_instance.findAppPage()
        time.sleep(12)
    
    def fill_out_mobile(self):
        try: 
            fields = self.driver.find_elements(By.CLASS_NAME, "jobs-easy-apply-form-section__grouping")
            for field in fields:

                if "Mobile phone number" in field.text:
                    field_input = field.find_element(By.TAG_NAME, "input")
                    field_input.clear()
                    field_input.send_keys(self.mobileNumber)

        except NoSuchElementException:
            print('no mobile number')
    
    def nextPage(self):

        time.sleep(3)

        self.jobIDs = []
        
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, ".jobs-search-pagination__button--next")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            element.click()
            time.sleep(5)
            return True

        except NoSuchElementException:
            return False
        

my_instance = botClass()

my_instance.login()
my_instance.choosePositionLocation()
my_instance.findAppPage()

applying = True

while (applying):

    my_instance.scroll()
    my_instance.applyLoop()

    if my_instance.nextPage():
        my_instance.pageNumber += 1
        pass
    else:
        my_instance.pageNumber = 0
        my_instance.choosePositionLocation()
        my_instance.findAppPage()
