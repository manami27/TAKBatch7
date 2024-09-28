import csv
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class DemoWebShopTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Inisialisasi Chrome WebDriver
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)  # Agar browser tetap terbuka setelah tes
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.get('https://demowebshop.tricentis.com/')
        assert 'Demo Web Shop' in cls.driver.title  # Memastikan judul halaman sesuai

    def register_user(self, first_name, last_name, email, password):
        try:
            # Klik tautan login dan kemudian Register
            self.driver.find_element(By.XPATH, '//a[@class="ico-login"]').click()
            self.driver.find_element(By.XPATH, '//input[@value="Register"]').click()

            # Isi formulir pendaftaran
            self.driver.find_element(By.XPATH, '//input[@id="gender-male"]').click()
            self.driver.find_element(By.XPATH, '//input[@id="FirstName"]').send_keys(first_name)
            self.driver.find_element(By.XPATH, '//input[@id="LastName"]').send_keys(last_name)
            self.driver.find_element(By.XPATH, '//input[@id="Email"]').send_keys(email)
            self.driver.find_element(By.XPATH, '//input[@id="Password"]').send_keys(password)
            self.driver.find_element(By.XPATH, '//input[@id="ConfirmPassword"]').send_keys(password)

            # Kirim formulir pendaftaran
            self.driver.find_element(By.XPATH, '//input[@id="register-button"]').click()

            # Cek apakah registrasi berhasil dengan memeriksa tombol "Continue"
            try:
                continue_button = self.driver.find_element(By.XPATH, '//input[@value="Continue"]')
                continue_button.click()
                print(f"Registration successful for {email}!")
            except NoSuchElementException:
                # Jika tombol "Continue" tidak ditemukan, registrasi mungkin gagal
                print(f"Registration failed for {email}. Checking for error messages...")
                self.check_error_messages()

            # Kembali ke homepage setelah registrasi
            self.driver.get('https://demowebshop.tricentis.com/')

        except NoSuchElementException as e:
            print(f"An error occurred during the registration process for {email}: {e}")

    def check_error_messages(self):
        # Fungsi untuk mencari pesan kesalahan
        error_messages = []
        error_fields = [
            'FirstName', 'LastName', 'Email', 'Password', 'ConfirmPassword'
        ]
        
        for field in error_fields:
            try:
                error_message_element = self.driver.find_element(By.XPATH, f'//span[@for="{field}"]')
                error_messages.append(error_message_element.text)
            except NoSuchElementException:
                pass
        
        try:
            # Pesan kesalahan spesifik untuk email sudah ada
            email_exists_element = self.driver.find_element(By.XPATH, '//li[normalize-space()="The specified email already exists"]')
            error_messages.append(email_exists_element.text)
        except NoSuchElementException:
            pass

        # Cek apakah ada pesan kesalahan yang ditemukan
        if error_messages:
            print(f"Error messages found: {', '.join(error_messages)}")
        else:
            print("No specific error message found.")

    def test_register_users_from_csv(self):
        # Membaca data dari file CSV dan menggunakan fungsi registrasi
        with open('register_data.csv', newline='') as csvfile:
            data_reader = csv.DictReader(csvfile)
            for row in data_reader:
                first_name = row['first_name']
                last_name = row['last_name']
                email = row['email']
                password = row['password']
                
                print(f"Registering user {first_name} {last_name} with email {email}")
                self.register_user(first_name, last_name, email, password)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()  # Tutup driver setelah semua tes selesai

if __name__ == "__main__":
    unittest.main()
