from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import glob
import time
import random
import requests


profile_id = ''

req_url = f"http://localhost:3001/v1.0/browser_profiles/{profile_id}/start/?automation=1"

response = requests.get(req_url)

response_json = response.json()
# print(response_json)

port = str(response_json['automation']['port'])
# print(port)

chrome_driver_path = Service('chromedriver')
chrome_options = webdriver.ChromeOptions()
chrome_options.debugger_address = '127.0.0.1:' + port
# chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--window-size=800,600")


# with open('messages.txt', 'r', encoding="utf8") as f:
    # messages = f.read().splitlines()
directory_path = "novitskyi_rmp∕"

class InstagramAutoposter():
    def __init__(self):
        self.driver = webdriver.Chrome(service=chrome_driver_path, options=chrome_options)

    def open_instagram(self):
        self.driver.get("https://www.instagram.com/mg_autola/")

    def login(self, username, password):
        username_field = self.driver.find_element(By.CSS_SELECTOR, 'input[name="username"]')
        password_field = self.driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')

        username_field.send_keys(username)
        password_field.send_keys(password)

        login_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        login_button.click()


    def get_file_paths(directory):
        file_paths = []
        for filename in os.listdir(directory):
            if filename.endswith(".jpg"):
                # Извлеките имя файла без расширения
                name_without_extension = os.path.splitext(filename)[0]
                # Проверьте, соответствует ли имя файла шаблону UTC_1/9
                if name_without_extension.endswith("_UTC") and name_without_extension[-6:-4].isdigit():
                    # Получите номер поста из имени файла
                    post_number = int(name_without_extension[-6:-4])
                    # Создайте путь к файлу и добавьте его в список file_paths
                    file_path = os.path.join(directory, filename)
                    file_paths.append(file_path)
        return file_paths



    def go_create(self):
        create_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "svg._ab6-[aria-label='New post']"))
        )
        # self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[7]/div/div/a/div')
        create_button.click()
        
        
    def go_multiple_files_input(self):
        
        # file_input = self.driver.find_element(By.CSS_SELECTOR, "form[enctype='multipart/form-data'][method='POST'][role='presentation']")
        upload_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button._acan._acap._acas._aj1-[type='button']"))
        )
        upload_button.click()
        
        for file_path in file_paths:
            upload_button.send_keys(file_path + Keys.ENTER)
        
        
    def close_poster(self):
        self.driver.close()
        self.driver.quit()


    def close_instagram(self):
        self.driver.quit()
        
    
    def auto_post_from_directory(self, directory):
        photo_files = glob.glob(os.path.join(directory, "*.jpg"))
        text_files = glob.glob(os.path.join(directory, "*.txt"))

        for text_file in text_files:
            caption = self.read_caption_from_file(text_file)
            print(f"CAPTION: \n{caption}")
            matching_photos = [photo_file for photo_file in photo_files if self.is_matching_photo(text_file, photo_file)]

            if caption and matching_photos:
                photo_path = random.choice(matching_photos)

                try:
                    print("Try upload photos")
                    self.upload_photo(photo_path, caption)
                    time.sleep(2)
                    try:
                        self.say_hello()
                        time.sleep(1)
                    except Exception as e:
                        print(e)
                        continue
                except Exception as e:
                    print(e)
                    break
                    self.close_poster()

    def read_caption_from_file(self, file_path):
        with open(file_path, 'r', encoding="utf8") as f:
            caption = f.read().strip()
        return caption

    def is_matching_photo(self, text_file, photo_file):
        base_name = os.path.splitext(text_file)[0]
        return base_name in photo_file
