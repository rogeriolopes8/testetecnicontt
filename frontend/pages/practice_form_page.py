from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


class PracticeFormPage:
    URL = "https://demoqa.com/automation-practice-form"

    # Locators
    FIRST_NAME = (By.ID, "firstName")
    LAST_NAME = (By.ID, "lastName")
    EMAIL = (By.ID, "userEmail")
    GENDER_MALE = (By.CSS_SELECTOR, "label[for='gender-radio-1']")
    MOBILE = (By.ID, "userNumber")

    DATE_INPUT = (By.ID, "dateOfBirthInput")
    DATE_MONTH_SELECT = (By.CLASS_NAME, "react-datepicker__month-select")
    DATE_YEAR_SELECT = (By.CLASS_NAME, "react-datepicker__year-select")

    SUBJECTS_INPUT = (By.ID, "subjectsInput")
    HOBBY_SPORTS = (By.CSS_SELECTOR, "label[for='hobbies-checkbox-1']")

    UPLOAD_PICTURE = (By.ID, "uploadPicture")
    CURRENT_ADDRESS = (By.ID, "currentAddress")

    STATE_CONTAINER = (By.ID, "state")
    STATE_DROPDOWN = (By.ID, "react-select-3-input")
    CITY_CONTAINER = (By.ID, "city")
    CITY_DROPDOWN = (By.ID, "react-select-4-input")

    SUBMIT_BUTTON = (By.ID, "submit")

    # Modal (vamos esperar pelo título com o texto padrão)
    MODAL_TITLE_XPATH = (
        By.XPATH,
        "//div[contains(@class,'modal-title') and contains(., 'Thanks for submitting')]"
    )
    RESULT_ROWS = (By.CSS_SELECTOR, "table tbody tr")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.URL)
        self.driver.maximize_window()
        self.remove_ads()

    # --- Helpers de layout / anúncios ---

    def remove_ads(self):
        """Remove banners fixos que atrapalham o clique no Submit."""
        script = """
            var ids = ['fixedban', 'close-fixedban'];
            ids.forEach(function(id){
                var el = document.getElementById(id);
                if (el) { el.remove(); }
            });
        """
        try:
            self.driver.execute_script(script)
        except Exception:
            pass

    # --- Preenchimento de campos ---

    def set_name(self, first_name: str, last_name: str):
        self.driver.find_element(*self.FIRST_NAME).send_keys(first_name)
        self.driver.find_element(*self.LAST_NAME).send_keys(last_name)

    def set_email(self, email: str):
        self.driver.find_element(*self.EMAIL).send_keys(email)

    def select_gender_male(self):
        elem = self.driver.find_element(*self.GENDER_MALE)

        # garante que o elemento está visível na tela
        self.driver.execute_script("arguments[0].scrollIntoView(true);", elem)

        # remove banners/ads que possam estar na frente
        self.remove_ads()

        # clique via JavaScript para evitar ElementClickInterceptedException
        self.driver.execute_script("arguments[0].click();", elem)


    def set_mobile(self, mobile: str):
        self.driver.find_element(*self.MOBILE).send_keys(mobile)

    def set_birth_date(self, day: int, month_index: int, year: int):
        """
        month_index: 0 = Jan, 9 = Oct etc.
        """
        self.driver.find_element(*self.DATE_INPUT).click()
        month_select = Select(self.driver.find_element(*self.DATE_MONTH_SELECT))
        year_select = Select(self.driver.find_element(*self.DATE_YEAR_SELECT))
        month_select.select_by_index(month_index)
        year_select.select_by_value(str(year))
        day_locator = (
            By.XPATH,
            f"//div[contains(@class,'react-datepicker__day') and text()='{day}' "
            "and not(contains(@class, 'react-datepicker__day--outside-month'))]"
        )
        self.driver.find_element(*day_locator).click()

    def set_subject(self, subject: str):
        elem = self.driver.find_element(*self.SUBJECTS_INPUT)
        elem.send_keys(subject)
        elem.send_keys(Keys.ENTER)

    def select_hobby_sports(self):
        self.driver.find_element(*self.HOBBY_SPORTS).click()

    def upload_picture(self, file_path: str):
        self.driver.find_element(*self.UPLOAD_PICTURE).send_keys(file_path)

    def set_current_address(self, address: str):
        self.driver.find_element(*self.CURRENT_ADDRESS).send_keys(address)

    def select_state(self, state: str):
        # clica no container pra abrir o dropdown e depois digita
        self.driver.find_element(*self.STATE_CONTAINER).click()
        state_input = self.driver.find_element(*self.STATE_DROPDOWN)
        state_input.send_keys(state)
        state_input.send_keys(Keys.ENTER)

    def select_city(self, city: str):
        self.driver.find_element(*self.CITY_CONTAINER).click()
        city_input = self.driver.find_element(*self.CITY_DROPDOWN)
        city_input.send_keys(city)
        city_input.send_keys(Keys.ENTER)

    # --- Submit & Modal ---

    def submit(self):
        button = self.driver.find_element(*self.SUBMIT_BUTTON)

        # garante que está visível
        self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
        self.remove_ads()

        # tentativa de clique normal
        try:
            ActionChains(self.driver).move_to_element(button).click().perform()
        except Exception:
            # fallback: clique via JavaScript
            self.driver.execute_script("arguments[0].click();", button)

    def wait_for_modal(self, timeout: int = 30):
        # espera pelo título padrão do modal
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.visibility_of_element_located(self.MODAL_TITLE_XPATH))

    def get_submission_table(self) -> dict:
        rows = self.driver.find_elements(*self.RESULT_ROWS)
        result = {}
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 2:
                key = cells[0].text.strip()
                value = cells[1].text.strip()
                result[key] = value
        return result
