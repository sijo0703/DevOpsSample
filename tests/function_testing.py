import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class TestUserManagement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up Chrome WebDriver
        cls.driver = webdriver.Chrome()
        cls.driver.get("http://127.0.0.1:5000")

    def test_add_user(self):
        driver = self.driver
        add_user_link = driver.find_element(By.LINK_TEXT, "Add New User")
        add_user_link.click()
        time.sleep(3)
        user_id_input = driver.find_element(By.NAME, "userid")
        user_id_input.send_keys("114")
        user_id_input.send_keys(Keys.RETURN)
        time.sleep(5)
        user_name_input = driver.find_element(By.NAME, "username")
        user_name_input.send_keys("Test4User")
        user_name_input.send_keys(Keys.RETURN)
        time.sleep(5)
        creation_date_input = driver.find_element(By.NAME, "creationdate")
        creation_date_input.send_keys("10/23/2024")
        user_name_input.send_keys(Keys.RETURN)
        time.sleep(5)
        # Verify the user is added
        self.assertIn("Test4User", driver.page_source)

    def test_update_user(self):
        driver = self.driver
        # Find the update form for the user
        #update_user_link = driver.find_element(By.LINK_TEXT, "Edit")
        #update_user_link.click()
        update_user_link = driver.find_element(By.XPATH, '//a[@href="/edit_user/101"]')
        update_user_link.click()
        time.sleep(3)
        update_input = driver.find_element(By.NAME, "username")
        update_input.clear()
        update_input.send_keys("UpdatedUser3")
        time.sleep(3)
        update_input.send_keys(Keys.RETURN)
        time.sleep(3)
        # Verify the user_name is updated
        self.assertIn("UpdatedUser3", driver.page_source)

    def test_delete_user(self):
        driver = self.driver
        #delete_link = driver.find_element(By.XPATH, '//a[@href="/delete/1"]')
        #delete_link.click()
        delete_user = driver.find_element(By.XPATH, '//form[@action="/delete_user/111"]')
        delete_user.click()
        time.sleep(5)
        # Verify the user is deleted
        self.assertNotIn("Test1User", driver.page_source)



    @classmethod
    def tearDownClass(cls):
        # Close the browser window after all tests
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
