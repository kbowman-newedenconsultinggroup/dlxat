import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def parse_date_to_nz_format(date_str):
    """Convert a date string like 'August 24, 2021' to '24/08/2021'."""
    try:
        # Parse the date string (e.g., "August 24, 2021") into a datetime object
        date_obj = datetime.strptime(date_str, "%B %d, %Y")
        # Format it to DD/MM/YYYY
        return date_obj.strftime("%d/%m/%Y")
    except ValueError:
        # Return the original string if parsing fails
        return date_str

def check_warranty_date(serial_number, driver):
    try:
        driver.get("https://support.hp.com/nz-en/check-warranty")
        
        wait = WebDriverWait(driver, 10)
        print(f"Entering serial number: {serial_number}")
        serial_input = wait.until(EC.presence_of_element_located((By.ID, "inputtextpfinder")))
        
        serial_input.clear()
        serial_input.send_keys(serial_number)
        
        print(f"Clicking submit button")
        submit_button = driver.find_element(By.ID, "FindMyProduct")
        submit_button.click()
        
        # Wait for the warranty result section to load
        wait.until(EC.presence_of_element_located((By.ID, "warrantyStatus")))
        
        # Try to get warranty end date with more flexible XPath
        try:
            print(f"Looking for end date")
            warranty_end_element = driver.find_element(
                By.XPATH, 
                "//*[contains(text(), 'End date') or contains(text(), 'end date') or contains(text(), 'Expiry') or contains(text(), 'expiration')]/following-sibling::*"
            )
            warranty_end = warranty_end_element.text.strip()
            if not warranty_end:
                warranty_end = "Not found (empty)"
            else:
                # Convert to NZ date format if it's a valid date
                warranty_end = parse_date_to_nz_format(warranty_end)
        except:
            print(f"End date not found, inspecting page")
            try:
                no_warranty = driver.find_element(By.XPATH, "//*[contains(text(), 'No warranty')]")
                warranty_end = "No warranty found"
            except:
                warranty_end = "Not found"
        
        return {
            "serial_number": serial_number,
            "warranty_expiry": warranty_end
        }
    
    except Exception as e:
        print(f"Error processing {serial_number}: {str(e)}")
        return {
            "serial_number": serial_number,
            "warranty_expiry": "Not Found"
        }

def process_csv(input_file, output_file):
    driver = setup_driver()
    results = []
    
    try:
        with open(input_file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header if it exists
            serial_numbers = [row[0] for row in reader]
        
        for serial in serial_numbers:
            if serial.strip():
                print(f"Checking serial number: {serial}")
                result = check_warranty_date(serial.strip(), driver)
                results.append(result)
                time.sleep(2)  # Delay to avoid overwhelming the server
        
        with open(output_file, 'w', newline='') as csvfile:
            fieldnames = ['serial_number', 'warranty_expiry']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        
        print(f"Results saved to {output_file}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    input_csv = "serial_numbers.csv"
    output_csv = f"warranty_dates_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    process_csv(input_csv, output_csv)