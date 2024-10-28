# frontend_testing.py
# webdriver_manager to automatically manage the ChromeDriver version, so you don’t have to manually download it.
# You can change this to Firefox or another browser if needed.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Function to start the WebDriver session
def start_session():
    # Setting up Chrome WebDriver (automatically downloads the driver if not available)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Replace with your web interface URL and user id
    web_interface_url = 'http://127.0.0.1:5000'  # Change to the actual web interface URL
    # user_id = 'sijoy'  # Change to the actual user id

    # Navigate to the web interface URL
    driver.get(web_interface_url)

    # Wait for a few seconds for the page to load
    time.sleep(10)  # Adjust the sleep time based on the page load speed

    try:
        # Locate the username element (example locator, adjust according to the actual web page)
        user_name_elements = driver.find_elements(By.ID, "col2") # Adjust the ID accordingly
        #print(user_name_elements)
        # Check if the element is displayed
        user_flag = False
        for user_to_check in user_name_elements:
            if user_to_check.text == "jisha":
                print("username element found.")
                # Print the username
                user_name = user_to_check.text
                print(f"User name: {user_name}")
                user_flag = True
                break
            else:
                user_flag = False
        if not user_flag:
            print("username element not found")

    except Exception as e:
        print(f"An error occurred: {e}")

    # Close the browser session
    driver.quit()

if __name__ == '__main__':
    start_session()
