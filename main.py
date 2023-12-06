# Modules required
# pip install selenium==4.13.0
from typing import List

VIDEO_PATH = r"C:\Users\bened\OneDrive\Desktop\Ben\fire2023\WhatsApp Video 2023-08-10 at 17.25.50.mp4"
PHOTU_PATH = r"assets/image/poster1.png"
PHOTU2_PATH = r"C:\Users\bened\OneDrive\Desktop\Ben\fire2023\WhatsApp Image 2023-08-09 at 10.33.25.jpg"

VIDEO_TEXT = """Jai Yeshu!

🥳जाgo...जाgo...जाgo🥳

Missed out on World Youth Day?

Join us for Mini-WYD in Bangalore!

What are you waiting for?

Register now!

http://bit.ly/MumbaiJaagoRegistration

For any query please contact. 

Jennifer- 97690 31785
Abhishek - 93726 25094

Chalo chalthe hai saath mai जाgo ke liye
"""

PHOTU2_TEXT = """🥳जाgo...जाgo...जाgo🥳

Abhi tak register nahi Kiya toh kya kiya?? 🫣

The last date for registration for the जाgo National Conference is 15th August, 2023!!!😱

Register now!

http://bit.ly/MumbaiJaagoRegistration

For any query please contact. 

Jennifer- 97690 31785
Abhishek - 93726 25094

Chalo chalthe hai saath mai जाgo ke liye
"""
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

import csv


# Waits for an element to appear and returns that element
def wait_for_element(by: By, string: str) -> WebElement:
    print(f"Waiting for {string}")
    while True:
        try:
            element = driver.find_element(by, string)
            break
        except:
            pass
    return element

# Waits for elements to appear and returns that element
def wait_for_elements(by: By, string: str) -> List[WebElement]:
    print(f"Waiting for {string}")
    while True:
        try:
            elements = driver.find_elements(by, string)
            break
        except:
            pass
    return elements


# Waits for an element to disappear if it exists
def wait_for_element_to_disappear(by: By, string: str):
    while True:
        try:
            elements = driver.find_elements(by, string)
            if len(elements) == 0:
                break
        except:
            pass


# Inserts text into text box
def paste_content(element: WebElement, content: str):
    driver.execute_script(
        f'''
const text = {content};
const dataTransfer = new DataTransfer();
dataTransfer.setData('text', text);
const event = new ClipboardEvent('paste', {{
  clipboardData: dataTransfer,
  bubbles: true
}});
arguments[0].dispatchEvent(event)
''',
        element)

def get_last_message() -> WebElement:
    messages = wait_for_elements(By.XPATH, '//div[@role="application"]/div[@role="row"]/div')
    while len(messages) <= 0:
        print("Waiting for messages to load")
        messages = wait_for_elements(By.XPATH, '//div[@role="application"]/div[@role="row"]/div')
    return messages[-1]

def wait_for_last_message_change(last_message):
    new_last_message = get_last_message()
    while new_last_message == last_message:
        print('Waiting for last message change')
        new_last_message = get_last_message()

# Sends a media. Returns when media is sent
def send_media(path_to_file, text=None):
    wait_for_element(By.XPATH, '//div[@aria-label="Attach"]').click()
    wait_for_element(By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]').send_keys(
        path_to_file)
    wait_for_element(By.XPATH, '//div[@role="presentation"]')
    if text:
        paste_content(wait_for_element(By.XPATH, '//div[@title="Type a message"]'), text)
    last_message = get_last_message()
    wait_for_element(By.XPATH, '//div[@aria-label="Send"]').click()
    wait_for_last_message_change(last_message)
    wait_for_element_to_disappear(By.XPATH, '//span[@aria-label=" Pending "]')


# Sends a text. Returns when text is sent
def send_text(text):
    paste_content(wait_for_element(By.XPATH, '//div[@title="Type a message"]'), text)
    last_message = get_last_message()
    wait_for_element(By.XPATH, '//button[@aria-label="Send"]').click()
    wait_for_last_message_change(last_message)
    wait_for_element_to_disappear(By.XPATH, '//span[@aria-label=" Pending "]')


# Parses the given number to countryCode + Number
def parse_number(number):
    raw_no = number.replace(" ", "")
    raw_no = raw_no.replace('+', "")
    phone = None
    if (len(raw_no) == 12 and raw_no.startswith('91')):
        phone = raw_no
    elif (len(raw_no) == 11 and raw_no.startswith('0')):
        phone = raw_no[1:]
    elif (len(raw_no) == 10):
        phone = '91' + raw_no
    return phone


driver = webdriver.Chrome()
driver.get("https://web.whatsapp.com/")
wait_for_element(By.XPATH, '//canvas[@role="img"]')
wait_for_element(By.XPATH, '//div[@role="textbox" and @contenteditable="true"]')

# Reads data from CSV
with open('data.csv') as file_obj:
    reader_obj = csv.reader(file_obj)

    # Iterate over each row in the csv
    # file using reader object
    for row in reader_obj:
        phone = parse_number(row[5])
        gender = row[8]
        # Sends only if person is female
        if phone and gender == 'Female':
            # Extract fist name from CSV
            first_name = row[1].strip().split(' ')[0]
            # Navigate to their chat
            driver.get(f"https://web.whatsapp.com/send/?phone={phone}&text&type=phone_number&app_absent=0")
            # Wait for chat to load
            textbox = wait_for_element(By.XPATH, '//div[@title="Type a message"]')
            # Send message
            send_media(PHOTU_PATH)
            send_media(VIDEO_PATH, VIDEO_TEXT)
            send_media(PHOTU2_PATH, PHOTU2_TEXT)