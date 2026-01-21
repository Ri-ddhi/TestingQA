import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

WATCH_MODE = True  

def human_delay(seconds=1):
    if WATCH_MODE:
        time.sleep(seconds)

def slow_type(element, text):
    for char in text:
        element.send_keys(char)
        if WATCH_MODE:
            time.sleep(0.05) 

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 5)

def take_screenshot(test_name):
    filename = f"{test_name}.png"
    driver.save_screenshot(filename)
    print(f"SCREENSHOT TAKEN: {filename}")

def handle_result_popup(test_type):
    try:
        # Check for Success Alert
        alert = wait.until(EC.alert_is_present())
        print(f"SUCCESS: {alert.text}")
        human_delay(1.5)
        alert.accept()
        take_screenshot(f"{test_type}_SUCCESS")
    except TimeoutException:
        try:
            error_msg = driver.find_element(By.ID, "message")
            print(f"ERROR CAPTURED: {error_msg.text}")
            take_screenshot(f"{test_type}_ERROR")
        except:
            print("No response message found.")

def run_registration(user, pw, cc, tel, test_label):
    driver.get("https://chulo-solutions.github.io/qa-internship/")
    
    u_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    p_field = driver.find_element(By.NAME, "password")
    c_field = driver.find_element(By.XPATH, "//label[contains(text(), 'Credit Card')]/following::input[1]")
    t_field = driver.find_element(By.XPATH, "//label[contains(text(), 'Telephone')]/following::input[1]")

    slow_type(u_field, user)
    slow_type(p_field, pw)
    slow_type(c_field, cc)
    slow_type(t_field, tel)
    
    human_delay(1)
    driver.find_element(By.XPATH, "//button[text()='Submit']").click()
    handle_result_popup(test_label)

try:
    # 1. POSITIVE TEST 
    print("\n--- Running Positive Test ---")
    run_registration("Riddhima12", "P@ssword1", "4242424242424242", "(555) 015-2667", "POSITIVE")

    # 2. NEGATIVE TESTS 
    negative_scenarios = [
        ("Ri@25", "P@ssword1", "4242424242424242", "(555) 015-2667", "NONALPHANUMERIC_USER"),
        ("Riddhima12", "p@ss12345", "4242424242424242", "(555) 015-2667", "NOUPPERCASE_PASSWORD"),
        ("Riddhima12", "P@ssword1", "4242424242 424242", "(555) 512-5444", "INVALID_CC"),
        ("Riddhima12", "P@ssword1", "4242424242424242", "(555) AB1-2667", "INVALID_TELEPHONE")

    ]

    for u, p, c, t, label in negative_scenarios:
        print(f"\n--- Running Negative Test: {label} ---")
        run_registration(u, p, c, t, label)

finally:
    human_delay(2)
    driver.quit()

