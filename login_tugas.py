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

    def login(self, username, password, expected_error_msg=None):
        try:
            # Klik tautan login
            self.driver.find_element(By.XPATH, '//a[@class="ico-login"]').click()

            # Masukkan username dan password
            self.driver.find_element(By.XPATH, '//input[@id="Email"]').send_keys(username)
            self.driver.find_element(By.XPATH, '//input[@id="Password"]').send_keys(password)

            # Kirim formulir login
            self.driver.find_element(By.XPATH, '//input[@value="Log in"]').click()

            # Cek jika login berhasil dengan mencari tautan logout
            try:
                self.driver.find_element(By.XPATH, '//a[@class="ico-logout"]')
                print(f"Login successful for {username}")
            except NoSuchElementException:
                # Cek pesan kesalahan jika login gagal
                try:
                    error_message_element = self.driver.find_element(By.XPATH, '//div[@class="validation-summary-errors"]')
                    error_message = error_message_element.text
                    if expected_error_msg and expected_error_msg in error_message:
                        print(f"Login failed for {username}: {error_message} (Expected message matched)")
                    else:
                        print(f"Login failed for {username}: {error_message} (Expected message did not match)")
                except NoSuchElementException:
                    print(f"Login failed for {username}, but no specific error message found.")

            # Log out setelah tes jika login berhasil
            try:
                self.driver.find_element(By.XPATH, '//a[@class="ico-logout"]').click()
            except NoSuchElementException:
                # Abaikan jika tidak ada opsi logout ditemukan (artinya login gagal)
                pass

        except NoSuchElementException as e:
            print(f"Error during login process for {username}: {e}")

        # Kembali ke homepage setelah login/logout
        self.driver.get('https://demowebshop.tricentis.com/')

    def test_login_from_csv(self):
        # Membaca data dari file CSV dan menggunakan fungsi login
        with open('login_data.csv', newline='') as csvfile:
            data_reader = csv.DictReader(csvfile)
            for row in data_reader:
                expected_error_msg = row.get('expected_error_msg', None)
                print(f"Testing login with Username: {row['username']} and Password: {row['password']}")
                self.login(row['username'], row['password'], expected_error_msg)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()  # Tutup driver setelah semua tes selesai

if __name__ == "__main__":
    unittest.main()
