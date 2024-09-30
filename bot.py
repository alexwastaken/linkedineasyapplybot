from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import logging

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
        self.positions = ["Full Stack", "Software Engineer", "Web Developer", "Front End Developer"]
        self.locations = ["Redmond, Wa", "San Diego, CA", "San Francisco, CA", "Austin, TX"]
        self.mobileNumber = "8582054657"
 
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
    
        random_number = random.randint(1, 3)
        self.position = self.positions[random_number]
        self.location = self.locations[random_number]

    def login(self):

        time.sleep(2)
        self.elem = self.driver.find_element(By.ID, "username")
        self.elem.send_keys("alexhparsons@gmail.com")
        time.sleep(1)
        self.elem = self.driver.find_element(By.ID, "password")
        self.elem.send_keys("Googleearth123!")
        self.elem = self.driver.find_element("xpath",'//*[@id="organic-div"]/form/div[3]/button')
        time.sleep(1)
        self.elem.click()
        time.sleep(20)

        return "logged in"
    
    def findAppPage(self):
        time.sleep(1)
        self.driver.get("https://www.linkedin.com/jobs/search/?keywords=" + self.position + "&location=" + self.location + "&start=0&f_AL=true")
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
                if "Easy Apply" in i.text:
                    self.jobIDs.append(i.get_attribute("data-job-id"))

        except Exception as e:
            logging.error(f"An error occurred during scrolling: {e}")

        time.sleep(12)




    def process_questions(self):
        time.sleep(0.5)
        try:
            # Locate all fields in the job application form
            form = self.driver.find_elements(By.XPATH, "//div[contains(@class,'jobs-easy-apply-form-section__grouping')]")
            
            for field in form:
                question = field.text.lower()
                answer = "yes"  # Set the answer to "Yes" for all radio buttons

                try:
                    # Handle checkboxes: Find all checkboxes and check them regardless of labels
                    checkboxes = field.find_elements(By.XPATH, ".//input[@type='checkbox']")
                    if checkboxes:
                        for checkbox in checkboxes:
                            if not checkbox.is_selected():
                                # Use JavaScript to check the checkbox
                                self.driver.execute_script("arguments[0].click();", checkbox)
                                print(f"Checked a checkbox for question: {question}")

                    # Handle radio buttons: Select the "Yes" option for all radio button questions
                    radio_buttons = field.find_elements(By.XPATH, ".//input[@type='radio']")
                    if radio_buttons:
                        for radio in radio_buttons:
                            # If the value is "yes" (case-insensitive), select it
                            if radio.get_attribute('value').strip().lower() == "yes":
                                # Use JavaScript to click the radio button
                                if not radio.is_selected():
                                    self.driver.execute_script("arguments[0].click();", radio)
                                    print(f"Selected 'Yes' for radio button question: {question}")
                                break  # Exit once "Yes" is found and clicked

                    # Handle dropdowns (multi-select)
                    dropdowns = field.find_elements(By.XPATH, ".//*[contains(@id, 'text-entity-list-form-component')]")
                    if dropdowns:
                        for dropdown in dropdowns:
                            options = dropdown.find_elements(By.TAG_NAME, "option")
                            if options:
                                selected_option = random.choice(options[:2])  # Randomly choose between first and second options
                                selected_option.click()
                                break

                    # Handle text inputs and text areas (if applicable)
                    text_inputs = field.find_elements(By.CSS_SELECTOR, "input[type='text'], textarea")
                    if text_inputs:
                        for text_input in text_inputs:
                            if text_input.get_attribute('value').strip():
                                print(f"Field already populated with: {text_input.get_attribute('value')}, skipping it.")
                                continue  # Skip if field is already populated

                            # Send the "Yes" answer or relevant input
                            text_input.send_keys(answer)

                            time.sleep(0.5)  # Allow time for the input to process

                            # Simulate down arrow and Enter to handle dropdowns, if applicable
                            text_input.send_keys(Keys.ARROW_DOWN)
                            text_input.send_keys(Keys.ENTER)

                except Exception as e:
                    print(f"Error processing field: {e}")
                    pass

        except Exception as e:
            print(f"Error: {e}")
            return

    def ans_question(self, question): #refactor this to an ans.yaml file
        answer = None
        if "how many" in question:
            answer = "1"
        elif "ever been employed" in question:
            answer = "no"
        elif "years of expierience" in question:
            answer = "3"
        elif "compensation" in question:
            answer = "100000"
        elif "salary" in question:
            answer = "100000"
        elif "website" in question:
            answer = "alexwastaken.com"
        elif "linkedin" in question:
            answer = "https://www.linkedin.com/in/ahparsons/"
        elif "currently employed by" in question:
            answer = "no"
        elif "experience" in question:
            answer = "1"
        elif "sponsor" in question:
            answer = "No"
        elif 'do you ' in question:
            answer = "Yes"
        elif "have you " in question:
            answer = "Yes"
        elif "US citizen" in question:
            answer = "Yes"
        elif "are you " in question:
            answer = "Yes"
        elif "salary" in question:
            answer = "90000"
        elif "can you" in question:
            answer = "Yes"
        elif "gender" in question:
            answer = "Male"
        elif "race" in question:
            answer = "Wish not to answer"
        elif "lgbtq" in question:
            answer = "Wish not to answer"
        elif "ethnicity" in question:
            answer = "Wish not to answer"
        elif "nationality" in question:
            answer = "Wish not to answer"
        elif "government" in question:
            answer = "I do not wish to self-identify"
        elif "are you legally" in question:
            answer = "Yes"
        elif "city" in question:
            answer = "San Diego"
        elif "hear about" in question:
            answer = "Linkedin"
        elif "start" in question:
            answer = "two weeks notice"
        elif "preferred name" in question:
            answer = "Alex"
        else:
            logging.info("Not able to answer question automatically. Please provide answer")
            #open file and document unanswerable questions, appending to it
            answer = "1"
            time.sleep(5)

            # df = pd.DataFrame(self.answers, index=[0])
            # df.to_csv(self.qa_file, encoding="utf-8")
        logging.info("Answering question: " + question + " with answer: " + answer)

        return answer

    def apply(self):

        try:
            # Wait until the apply button is clickable and click it
            apply_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "jobs-apply-button--top-card"))
            )
            apply_button.click()
            time.sleep(1)

            try:
                    # Try to find and click the button
                    susButton = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "jobs-apply-button"))
                    )
                    susButton.click()
                    print("Button clicked!")
            except:
                    # Ignore any errors and just continue the program
                pass


            time.sleep(1)

            # Fill out the application fields (assuming self.fill_out_fields is defined)
            self.fill_out_mobile()
            time.sleep(3)
            self.next_ButtonInitial = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Continue to next step']")
            self.next_ButtonInitial.click()
            time.sleep(1)

        except NoSuchElementException:
                print("'Review your application' button not found")

        # Start the loop until 'Submit' button is clicked
        self.attempts = 0
        while True:
            if ()
            self.attempts += 1
            # Try to click 'Continue to next step' button if it exists
            try:
                self.next_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Continue to next step']")
                
                if self.next_button.is_displayed():
                    print("Clicking 'Continue to next step'")
                    time.sleep(3)
                    self.process_questions()
                    self.next_button.click()
                    continue  # Go back to the start of the loop to check for the next step

            except NoSuchElementException:
                print("'Continue to next step' button not found")

            # Try to click 'Review your application' button if it exists
            try:
                self.review_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Review your application']")
                if self.review_button.is_displayed():
                    print("Clicking 'Review your application'")
                    self.process_questions()
                    self.review_button.click()
                    time.sleep(3)
                    continue  # Go back to the start of the loop to check for the next stepa

            except NoSuchElementException:
                print("'Review your application' button not found")

            # If 'Submit' button is found, click and exit the loop
            try:
                self.submit_container = self.driver.find_element(By.CLASS_NAME, "artdeco-modal__content")
                for i in range(300, 1000, 100):
                    self.driver.execute_script("arguments[0].scrollTo(0, arguments[1]);", self.submit_container, i)
                    time.sleep(0.1)  # Small delay to ensure new content loads
            

                self.follow_button = self.driver.find_element(By.CSS_SELECTOR, "label[for='follow-company-checkbox']")
                if self.follow_button.is_displayed():
                    self.follow_button.click()
                    print("Clicked follow company checkbox")

                self.submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Submit application']")
                if self.submit_button.is_displayed():
                    self.submit_button.click()
                    print("Application submitted")
                    break  # Exit the loop after submitting the application

            except NoSuchElementException as e:
                print("Submit button or follow checkbox not found:", e)
                break  # Exit loop if submit button is not found and there's no way to proceed




    def applyLoop(self):
        for x in self.jobIDs:
            self.driver.get(f"https://www.linkedin.com/jobs/view/{x}/")
            self.apply()
            time.sleep(6)
        self.jobIDs = []
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
        
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, ".jobs-search-pagination__button--next")

            element.click()
            time.sleep(5)
            return True

        except NoSuchElementException:
            return False
        

random_number = random.randint(1000000000, 9999999999)

my_instance = botClass(random_number)


my_instance.login()
my_instance.choosePositionLocation()
my_instance.findAppPage()

applying = True

while (applying):

    my_instance.scroll()
    my_instance.applyLoop()

    if my_instance.nextPage():
        pass
    else:
        my_instance.choosePositionLocation()
        my_instance.findAppPage()
