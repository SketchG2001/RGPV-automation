import os
import time
from PIL import Image, ImageOps
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytesseract

driver = webdriver.Chrome()
driver.get('https://www.rgpv.ac.in/Login/StudentLogin.aspx')

usernameField = driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_uc_UserLogin1_txtUserName"]')
passwordField = driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_uc_UserLogin1_txtPassword"]')
captchaField = driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_uc_UserLogin1_txtCaptcha"]')

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

captchaImage = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="ContentPlaceHolder1_uc_UserLogin1_pnlCaptcha"]/div[2]/div/span/div/img'))
)
captchaImage.screenshot('captcha.png')

image = Image.open('captcha.png')
image = image.convert("L")
image = ImageOps.invert(image)
image = image.point(lambda x: 0 if x < 140 else 255)
image.save('processed_captcha.png')

captchaText = pytesseract.image_to_string(image, config='--psm 6').strip()
print(f"Extracted CAPTCHA Text: {captchaText}")

usernameField.send_keys(os.environ.get('rollnum'))
passwordField.send_keys('Psjat@143',Keys.TAB)
captchaField.send_keys(captchaText)


actions = ActionChains(driver)
for char in captchaText:
    actions.send_keys(char)
    actions.pause(0.2)
actions.perform()

submitButton = driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_uc_UserLogin1_imgLogin"]')
time.sleep(2)
submitButton.click()

try:
    WebDriverWait(driver, 1000).until(EC.url_changes(driver.current_url))
    afterLogin = WebDriverWait(driver,100).until(
        EC.presence_of_element_located((By.XPATH,'//*[@id="ContentPlaceHolder1_uc_UserLogin1_imgLogin"]')))
    print(afterLogin.text)
    print("Login successful!")
except:
    print("Login failed. Check CAPTCHA or credentials.")

driver.quit()
