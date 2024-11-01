import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

class TestUserManagement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up Chrome WebDriver
        #cls.driver = webdriver.Chrome()
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.get("http://127.0.0.1:5000")

    def test_01_add_user(self):
        driver = self.driver
        add_user_link = driver.find_element(By.LINK_TEXT, "Add New User")
        add_user_link.click()
        time.sleep(3)
        user_id_input = driver.find_element(By.NAME, "userid")
        print()
        user_id_input.send_keys("2001")
        user_id_input.send_keys(Keys.RETURN)
        time.sleep(5)
        user_name_input = driver.find_element(By.NAME, "username")
        user_name_input.send_keys("TestUserJen")
        user_name_input.send_keys(Keys.RETURN)
        time.sleep(5)
        creation_date_input = driver.find_element(By.NAME, "creationdate")
        creation_date_input.send_keys("10/20/2024")
        user_name_input.send_keys(Keys.RETURN)
        time.sleep(5)
        # Verify the user is added
        self.assertIn("TestUserJen", driver.page_source)

    def test_02_update_user(self):
        driver = self.driver
        # Find the update form for the user
        #update_user_link = driver.find_element(By.LINK_TEXT, "Edit")
        #update_user_link.click()
        update_user_link = driver.find_element(By.XPATH, '//a[@href="/edit_user/2001"]')
        update_user_link.click()
        time.sleep(3)
        update_input = driver.find_element(By.NAME, "username")
        update_input.clear()
        update_input.send_keys("TestUserJenZ")
        time.sleep(3)
        update_input.send_keys(Keys.RETURN)
        time.sleep(3)
        # Verify the user_name is updated
        self.assertIn("TestUserJenZ", driver.page_source)

    def test_03_delete_user(self):
        driver = self.driver
        time.sleep(5)
        #delete_link = driver.find_element(By.XPATH, '//a[@href="/delete/1"]')
        #delete_link.click()
        delete_user = driver.find_element(By.XPATH, '//form[@action="/delete_user/2001"]')
        delete_user.click()

        # Verify the user is deleted
        self.assertNotIn("TestUserJenZ", driver.page_source)



    @classmethod
    def tearDownClass(cls):
        # Close the browser window after all tests
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()

