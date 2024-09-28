import csv
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up WebDriver with options
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

# Function to login to the account
def login(email, password):
    try:
        driver.get('https://demowebshop.tricentis.com/')
        assert 'Demo Web Shop' in driver.title  

        # Click login and enter email and password
        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="ico-login"]'))).click()
        wait.until(EC.presence_of_element_located((By.ID, 'Email'))).send_keys(email)
        wait.until(EC.presence_of_element_located((By.ID, 'Password'))).send_keys(password)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Log in"]'))).click()

        # Check if login was successful
        try:
            error_message_element = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="validation-summary-errors"]'))
            )
            error_message = error_message_element.text
            logging.error(f"Login failed: {error_message}")
            return False
        except TimeoutException:
            logging.info(f"Login successful for {email}")
            return True
    except Exception as e:
        logging.error(f"Error during login: {e}")
        return False

# Function to add product to cart
def add_product_to_cart(recipient_name, recipient_email, quantity):
    try:
        # Click gift card button
        wait.until(EC.element_to_be_clickable((By.XPATH, '//div[2]//div[1]//div[2]//div[3]//div[2]//input[1]'))).click()

        # Fill out gift card form
        wait.until(EC.presence_of_element_located((By.ID, 'giftcard_2_RecipientName'))).send_keys(recipient_name)
        wait.until(EC.presence_of_element_located((By.ID, 'giftcard_2_RecipientEmail'))).send_keys(recipient_email)

        quantity_element = wait.until(EC.presence_of_element_located((By.ID, 'addtocart_2_EnteredQuantity')))
        quantity_element.clear()
        quantity_element.send_keys(quantity)

        # Click "Add to Cart"
        wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="add-to-cart-button-2"]'))).click()
        logging.info(f"Gift card for {recipient_name} added to cart successfully.")
    except Exception as e:
        logging.error(f"Error adding product: {e}")

# Function to checkout
def checkout():
    try:
        # Open shopping cart
        wait.until(EC.element_to_be_clickable((By.XPATH, '//span[normalize-space()="Shopping cart"]'))).click()

        # Accept terms and conditions
        wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="termsofservice"]'))).click()

        # Click "Checkout"
        wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@id="checkout"]'))).click()

        # Fill in billing information and continue
        wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@title="Continue"]'))).click()

        # Select payment method
        wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="paymentmethod_0"]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@class="button-1 payment-method-next-step-button"]'))).click()

        # Continue payment information
        wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@class="button-1 payment-info-next-step-button"]'))).click()

        # Confirm order
        wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Confirm"]'))).click()

        # Click "Continue" after confirmation
        wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Continue"]'))).click()

        logging.info("Checkout successful.")
    except Exception as e:
        logging.error(f"Error during checkout: {e}")

# Read data from CSV and run tests
try:
    with open('test_data.csv', newline='') as csvfile:
        data_reader = csv.DictReader(csvfile)
        for row in data_reader:
            email = row['email']
            password = row['password']
            recipient_name = row['recipient_name']
            recipient_email = row['recipient_email']
            quantity = row['quantity']

            logging.info(f"Attempting to login with email: {email}")
            if login(email, password):
                logging.info(f"Adding product for {recipient_name} to cart.")
                add_product_to_cart(recipient_name, recipient_email, quantity)
                logging.info("Processing checkout.")
                checkout()
            else:
                logging.warning(f"Login failed for {email}, cannot proceed.")
finally:
    # Close the driver after all tests are complete
    driver.quit()
