from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from faker import Faker
from password_generator import PasswordGenerator
import time
import random
import unicodedata
from faker import Faker
import random



fake = Faker("de_DE")

def get_address():
    while True:
        address = fake.address()
        parts = address.split()
        if len(parts) <= 4:
            return parts[0], parts[1], parts[2], parts[3]

def get_name():
    while True:
        name = fake.name()
        parts = name.split()
        if len(parts) <= 2:
            return parts[0], parts[1]

street, snr, plz, city = get_address()
fname, lname = get_name()


print(lname)

pwo = PasswordGenerator()
password = pwo.generate()


endings = ["okaklsk-ss.net", "schneller-ccc.com", "schulenadressen.de", "heatmaps.net"]

random_ending = random.choice(endings)



def clean_email(email):
    parts = email.split('@')
    username = ''.join((c for c in unicodedata.normalize('NFD', parts[0]) if unicodedata.category(c) != 'Mn'))
    username = ''.join(e for e in username if e.isalnum() or e in ['.', '_'])
    

    cleaned_email = f"{username.lower()}@{parts[1]}"
    return cleaned_email


e_mail = clean_email(f"{fname.lower()}.{lname.lower()}@{random_ending}")
print(e_mail)
 


user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
chrome_options = Options()
chrome_options.add_argument(f"user-agent={user_agent}")


prefs = {
    #"profile.managed_default_content_settings.images": 2,  
    #"profile.managed_default_content_settings.javascript": 2,  
    #"profile.managed_default_content_settings.stylesheet": 2, 
    "profile.managed_default_content_settings.cookies": 2,  
    #"profile.managed_default_content_settings.plugins": 2,  
}
chrome_options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=chrome_options)



registration_link = "https://www.medimops.de/Registrierung/"
driver.get(registration_link)

coockie = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, "/html/body/div/div[2]/div/div[2]/button[1]"))
            )
coockie.click()

email_field = driver.find_element(By.ID, "email")

email_field.click()
email_field.send_keys(e_mail)

passwort_field = driver.find_element(By.NAME, "password")
passwort_field.send_keys(password)


password_field = driver.find_element(By.NAME, "passwordConfirm")
password_field.send_keys(password)

gender_button = driver.find_element(By.NAME, "gender")
gender_button.click()

fname_field = driver.find_element(By.ID, "firstname")
fname_field.send_keys(fname)

lname_field = driver.find_element(By.ID, "lastname")
lname_field.send_keys(lname)


street_field = driver.find_element(By.ID, "street")
street_field.send_keys(street)


snr_field = driver.find_element(By.ID, "streetnr")
snr_field.send_keys(snr)


zip_field = driver.find_element(By.ID, "zip")
zip_field.send_keys(plz)


city_field = driver.find_element(By.ID, "city")
city_field.send_keys(city)


time.sleep(1) 

driver.find_element(By.ID, "agb-check").submit()
time.sleep(10)

def save(e_mail, password):
    with open('konten.txt', 'a', encoding="utf-8") as file:
        file.write(f'{e_mail};{password}\n')


save(e_mail,password)


driver.quit()


