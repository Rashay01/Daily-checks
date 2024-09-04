from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import time
import pandas as pd

load_dotenv()

def bypass_security_warning(driver):
    try:
        # Wait for 50 seconds before attempting to click "Advanced"
        # time.sleep(50)

        # Wait for the "Advanced" button to be clickable and click it
        advanced_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[text()="Advanced"]'))
        )
        advanced_button.click()
        
        # Wait for the "Proceed to [site] (unsafe)" link to be clickable and click it
        proceed_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[text()="Proceed to [site] (unsafe)"]'))
        )
        proceed_link.click()

        print("Bypassed security warning and proceeded to the site.")
    
    except Exception as e:
        print(f"An error occurred while bypassing the security warning: {e}")

def click_element_by_text(driver, text):
    try:
        # Wait for any element with the specified text to be clickable
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f'//*[text()="{text}"]'))
        )

        # Click the element
        element.click()

        # Wait for new tab to open (optional: you can adjust this based on how long it typically takes)
        time.sleep(2)

        # Switch to the new tab
        driver.switch_to.window(driver.window_handles[-1])

        # Wait for the page to load fully (adjust as needed)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*'))
        )

        # # Take a screenshot
        # screenshot_path = f'screenshot_{text}.png'
        # driver.save_screenshot(screenshot_path)
        # print(f'Screenshot of the new tab saved as {screenshot_path}.')

    except Exception as e:
        print(f"An error on click: {text}")
        raise
    
def click_back_icon(driver):
    try:
        # Wait for the element with the specified class and style to be clickable
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'span.sapUshellShellHeadItmCntnt'))
        )

        # Click the element
        element.click()

        # Wait for new tab to open (optional: you can adjust this based on how long it typically takes)
        time.sleep(2)

        # Switch to the new tab (if a new tab is opened)
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-1])

            # Wait for the page to load fully (adjust as needed)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*'))
            )

            # Optionally, take a screenshot
            # screenshot_path = 'screenshot_new_tab.png'
            # driver.save_screenshot(screenshot_path)
            # print(f'Screenshot of the new tab saved as {screenshot_path}.')
        
    except Exception as e:
        print(f"An error occurred while clicking the element: {e}")
        raise
    
def click_element_by_id(driver, elementID, wait_for_element_xpath=None):
    try:
        # Wait for the element with the specified ID to be clickable
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, elementID))
        )

        # Click the element
        element.click()

        # Wait for a new tab to open
        WebDriverWait(driver, 10).until(
            EC.number_of_windows_to_be(2)
        )

        # Switch to the new tab
        driver.switch_to.window(driver.window_handles[-1])

        # Wait for the page to load fully or for a specific element to appear
        if wait_for_element_xpath:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, wait_for_element_xpath))
            )
        else:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*'))
            )

        # Optional: Take a screenshot
        # screenshot_path = f'screenshot_{elementID}.png'
        # driver.save_screenshot(screenshot_path)
        # print(f'Screenshot of the new tab saved as {screenshot_path}.')

    except Exception as e:
        print(f"An error occurred while clicking element with ID '{elementID}': {e}")
        raise

def click_element_by_text_js(driver, text, wait_time=10):
    """
    Clicks an element with the specified text using JavaScript.

    :param driver: Selenium WebDriver instance.
    :param text: Text of the element to be clicked.
    :param wait_time: Maximum time to wait for the page to load.
    """
    try:
        # Wait for the page to load
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.XPATH, '//*'))
        )

        # Use JavaScript to find and click the element
        script = f"""
        var elements = document.querySelectorAll('a');
        for (var i = 0; i < elements.length; i++) {{
            if (elements[i].innerText.includes("{text}")) {{
                elements[i].click();
                return;
            }}
        }}
        """
        driver.execute_script(script)
        print(f"Element with text '{text}' clicked successfully using JavaScript.")
    except Exception as e:
        print(f"An error occurred while clicking {text} with JavaScript: {e}")
        raise

def click_element_when_ready(driver, text, wait_time=10):
    """
    Waits for an element with the specified text to be clickable and clicks it.

    :param driver: Selenium WebDriver instance.
    :param text: Text of the element to be clicked.
    :param wait_time: Maximum time to wait for the element to be clickable.
    """
    try:
        # Wait for the element to be clickable
        element = WebDriverWait(driver, wait_time).until(
            EC.element_to_be_clickable((By.XPATH, f'//*[text()="{text}"]'))
        )
        element.click()
        print(f"Element with text '{text}' clicked successfully.")
    except Exception as e:
        print(f"An error occurred while waiting for and clicking {text}: {e}")
        raise

def scroll_and_click_by_text(driver, text, wait_time=10, max_scroll_attempts=20, scroll_increment=1):
    """
    Scrolls down the page incrementally until an element with the specified text is found and clicks it.

    :param driver: Selenium WebDriver instance.
    :param text: Text of the element to be clicked.
    :param wait_time: Maximum time to wait for the element to be present and clickable.
    :param max_scroll_attempts: Maximum number of incremental scrolls before giving up.
    :param scroll_increment: Amount of pixels to scroll per attempt.
    """
    try:
        # Initialize WebDriverWait
        wait = WebDriverWait(driver, wait_time)

        for attempt in range(max_scroll_attempts):
            # Wait for the element to be present
            try:
                element = wait.until(
                    EC.presence_of_element_located((By.XPATH, f'//*[text()="{text}"]'))
                )
                # Scroll to the element using JavaScript
                driver.execute_script("arguments[0].scrollIntoView(true);", element)

                # Optional: Wait a bit to ensure the scrolling is done
                time.sleep(5)

                # Click the element
                element.click()
                print(f"Element with text '{text}' clicked successfully.")
                return  # Exit the function after successful click
            except:
                # If the element is not found, scroll down incrementally and try again
                driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
                time.sleep(2)  # Wait for the page to load new content
        
        print(f"Element with text '{text}' not found after scrolling.")
    except Exception as e:
        print(f"An error occurred while scrolling and clicking {text}: {e}")
        raise

def click_image_by_id(driver, image_id, wait_time=10):
    try:
        # Wait for the image element to be present
        wait = WebDriverWait(driver, wait_time)
        image_element = wait.until(
            EC.presence_of_element_located((By.ID, image_id))
        )

        # Scroll to the image element using JavaScript
        driver.execute_script("arguments[0].scrollIntoView(true);", image_element)

        # Optional: Wait a bit to ensure the scrolling is done
        WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.ID, image_id))
        )

        # Click the image element
        image_element.click()
        print(f"Image with ID '{image_id}' clicked successfully.")

    except Exception as e:
        print(f"An error occurred in clicking image: {image_id}")
        raise

def click_button_by_value(driver, value):
    try:
        # Locate the button using the 'value' attribute
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f'//input[@type="submit" and @value="{value}"]'))
        )

        # Click the button
        button.click()

        # Wait for new tab to open (optional: you can adjust this based on how long it typically takes)
        time.sleep(2)

        # Switch to the new tab if applicable
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-1])

        # Wait for the page to load fully (adjust as needed)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*'))
        )

        print(f'Button with value "{value}" clicked.')

    except Exception as e:
        print(f"Error occurred while clicking the button with value '{value}'")
        # Reraise the exception to indicate failure
        raise


#-------------------------------------------------------------------------------------    
def selectDatabase(driver, groupName, databaseName,fileLocation):
    try:
        click_image_by_id(driver,"shell-header-icon")
        print(f"Click group {groupName}")
        click_element_by_text(driver, groupName)
        
        time.sleep(2)
        
        print(f"Scroll and click {databaseName}")
        click_element_by_text_js(driver, databaseName)
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*'))
        )
        time.sleep(20)
        
        print(f"Successfully selected database")
        save_screenshot(driver,"TestDB","databaseSelected.png")
        save_screenshot()
        print("databaseSelected Screenshot saved.")
    except Exception as e:
        print(f"Error occurred in Select Database")
    
def login(driver):
    try:
        # Load username and password from environment variables
        username = os.getenv('USERNAME_1')
        password = os.getenv('PASSWORD')

        # Locate the username and password input fields
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'username'))  # Adjust selector as needed
        )
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'password'))  # Adjust selector as needed
        )

        # Input the username and password
        username_field.send_keys(username)
        password_field.send_keys(password)

        # Submit the form or perform login action
        click_button_by_value(driver, "Log On")

        print("Logged in successfully.")
        

    except Exception as e:
        print(f"An error occurred during login: {e}")

def check_and_click_elements(driver, wait_time=10):
    try:
        # Wait for the presence of the text elements
        wait = WebDriverWait(driver, wait_time)
        
        # Check for the presence of the "Monitoring" text
        monitoring_element = wait.until(
            EC.presence_of_element_located((By.XPATH, '//span[text()="Monitoring"]'))
        )
        
        # If "Monitoring" is found, click the associated button
        if monitoring_element:
            print("Text 'Monitoring' found.")
            # Locate and click the button associated with "Monitoring"
            # 
            click_element_by_id(driver, '__xmlview38--idVariantManagement-trigger-img')
            # button = driver.find_element(By.XPATH, '//span[@id="__xmlview188--idVariantManagement-trigger-inner"]')
            # button.click()
            print("Button associated with 'Monitoring' clicked.")
        
        # Check for the presence of the "All" text
        
        # If "All" is found, click the associated element
            
        # click_element_by_text(driver, "All")
        click_element_by_id(driver,'__xmlview38--idVariantManagement-trigger-item-1')
        print("Element with text 'All' clicked.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

def search_input_field(driver, input_id, search_query, wait_for_element_xpath=None):
    """
    Searches using an <input> field identified by its ID and optionally waits for a specific element to appear.
    
    :param driver: The Selenium WebDriver instance.
    :param input_id: The ID of the <input> element used for search.
    :param search_query: The query string to send to the search input field.
    :param wait_for_element_xpath: Optional XPath of an element to wait for after performing the search.
    """
    try:
        # Wait for the <input> element with the specified ID to be visible and enabled
        input_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, input_id))
        )

        # Clear the input field (in case it contains any pre-existing value)
        input_field.clear()

        # Send the search query to the input field
        input_field.send_keys(search_query)

        # Optionally wait for a specific element or condition if provided
        if wait_for_element_xpath:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, wait_for_element_xpath))
            )

        # Optional: Take a screenshot
        # screenshot_path = f'screenshot_search_{search_query}.png'
        # driver.save_screenshot(screenshot_path)
        # print(f'Screenshot saved as {screenshot_path}.')

    except Exception as e:
        print(f"An error occurred while searching with input ID '{input_id}': {e}")
        raise  
    
def save_screenshot(driver, folder_path, file_name):
    """
    Takes a screenshot and saves it to a specified folder with a given file name.
    
    :param driver: The Selenium WebDriver instance.
    :param folder_path: The folder where the screenshot will be saved.
    :param file_name: The name of the screenshot file.
    """
    try:
        # Ensure the folder exists, create it if it does not
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Define the full path to save the screenshot
        screenshot_path = os.path.join(folder_path, file_name)

        # Save the screenshot
        driver.save_screenshot(screenshot_path)
        print(f'Screenshot saved as {screenshot_path}.')

    except Exception as e:
        print(f"An error occurred while saving the screenshot: {e}")
        raise 

def check_and_click_elements(driver, wait_time=10):
    try:
        # Wait for the presence of the text elements
        wait = WebDriverWait(driver, wait_time)
        
        # Check for the presence of the "Monitoring" text
        
        # If "Monitoring" is found, click the associated button
        
        click_element_by_id(driver, '__xmlview38--idVariantManagement-trigger-img')
        # button = driver.find_element(By.XPATH, '//span[@id="__xmlview188--idVariantManagement-trigger-inner"]')
        # button.click()
        print("Button associated with 'Monitoring' clicked.")
        time.sleep(4)
        
        # Check for the presence of the "All" text
        
        # If "All" is found, click the associated element
            
        # click_element_by_text(driver, "All")
        click_element_by_id(driver,'__xmlview38--idVariantManagement-trigger-item-1')
        print("Element with text 'All' clicked.")
        
        time.sleep(4)
    
    except Exception as e:
        print(f"An error occurred: {e}")
        raise


#---------------------------------------------------------
def create_excel_with_table_in_folder(folder_path, file_name):
    """
    Creates an Excel file with a predefined table in the specified folder.
    
    Args:
    folder_path (str): The path to the folder where the Excel file should be created.
    file_name (str): The name of the Excel file to be created.
    """
    # Ensure the folder exists
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Define the file path
    file_path = os.path.join(folder_path, file_name)

    # Check if the file already exists
    if os.path.exists(file_path):
        print(f"The file '{file_name}' already exists in the folder '{folder_path}'.")
        return  # Exit the function to avoid overwriting the file

    # Define the data
    data = {
        'Database check': [
            'Check if service interrupted/Any inconsistencies with logging on',
            'Memory/CPU usage',
            'Disk space usage',
            'DB lock check',
            'System Dumps',
            'Backup check',
            'Certificate check'
        ],
        'Monday': ['', '', '', '', '', '', ''],
        'Tuesday': ['', '', '', '', '', '', ''],
        'Wednesday': ['', '', '', '', '', '', ''],
        'Thursday': ['', '', '', '', '', '', ''],
        'Friday': ['', '', '', '', '', '', ''],
        'Saturday': ['', '', '', '', '', '', ''],
        'Sunday': ['', '', '', '', '', '', '']
    }

    # Create a DataFrame from the data
    df = pd.DataFrame(data)

    # Write the DataFrame to an Excel file
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Schedule', index=False)

    print(f"Excel file '{file_path}' created successfully with the table.")

def main():
    url = 'https://hanahcdbdev.mud.internal.co.za:39630/'  # Replace with the URL that triggers the warning

    # Set up Chrome options
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Optional: Run in headless mode (no GUI)
    chrome_options.add_argument("--ignore-certificate-errors")  # Ignore certificate errors
    chrome_options.add_argument("--start-maximized")
 
    # Start Chrome with a fresh profile to clear cache
    # chrome_options.add_argument("--incognito")

    # Automatically download and set up ChromeDriver (caching enabled)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    create_excel_with_table_in_folder("TestDB","Output.xlsx")

    try:
        # Open the website
        driver.get(url)

        # Bypass the security warning
        bypass_security_warning(driver)
        
        click_element_by_text(driver,"hana-cockpit")
        
        login(driver)
        
        save_screenshot(driver,"TestDB","login.png")
        print("Screenshot saved.")
        
        
        selectDatabase(driver,"Training", "TESTDB@DHB","TestDB")
        
        check_and_click_elements(driver)
        
        # Search for backups 
        search_input_field(driver, 'idSearchFieldOVP-I', 'backups')
        click_element_by_id(driver, "idSearchFieldOVP-search")
        
        time.sleep(4)
        
        click_element_by_text(driver,"Database ")
        time.sleep(4)
        
        save_screenshot(driver,"TestDB","Backups.png")
        # while True:
        
        click_back_icon(driver)
        time.sleep(4)
        
        # Search for CPU 
        search_input_field(driver, 'idSearchFieldOVP-I', 'CPU')
        click_element_by_id(driver, "idSearchFieldOVP-search")
        
        time.sleep(10)
        
        save_screenshot(driver,"TestDB","CPU.png")
        print("Screenshot saved.")
        

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    main()
