from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
pwd = os.getcwd()
lecture_id = int(pwd.split('/')[-1].split('lec')[-1])
driver.get(f"https://jyywiki.cn/OS/2024/lect{lecture_id}.md")

wait = WebDriverWait(driver, 5)

buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.hover\\:bg-blue-300")))
code_texts = []
for button in buttons:
    button.click()
    sleep(0.15)
    text = driver.find_elements(By.CLASS_NAME, "select-all")[0].text
    code_texts.append(text)
    driver.find_element(By.CSS_SELECTOR, "button.px-4").click()

driver.quit()

for code in code_texts:
    print(code)
    os.system(code)