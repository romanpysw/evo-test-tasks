import csv
import os
from time import sleep

from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

"""Список прокси, нужно заполнить стабильными рабочими IP прокси"""
proxy_bank = [
#    '51.161.9.105:8080',
#    '51.161.9.105:8080'
]
url = 'https://www.nseindia.com/'


def nseindia_simulation(url):

    """Создание csv"""
    wFile = open("nseindia_res.csv", mode = "w", encoding = 'utf-8')
    names = ["Наименование", "Цена"]
    file_writer = csv.DictWriter(wFile, delimiter = ';', lineterminator = '\n', fieldnames = names)
    file_writer.writeheader()

    """Заполнение драйвера и его опций"""
    useragent = UserAgent()
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={useragent.random}")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("start-maximized")

    """Раскомментировать строку ниже, если есть стабильные прокси, тогда каждая сессия будет со случайного IP"""
#    options.add_argument(f"--proxy-server={random.choice(proxy_bank)}")

    
    driver = webdriver.Chrome(
        executable_path=os.getcwd() + '/chromedriver.exe', 
        options=options
    )

    try:
        """Заходим на nseindia"""
        driver.get(url)

        sleep(2)

        """Наводимся на MARKET DATA"""
        driver.delete_all_cookies()
        market_data_button = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="main_navbar"]/ul/li[3]/a')))
        hover = ActionChains(driver).move_to_element(market_data_button).perform()

        sleep(2)

        """Наводимся и переходим на Pre-Open Market"""
        pre_open_market = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main_navbar"]/ul/li[3]/div/div[1]/div/div[1]/ul/li[1]/a')))
        pre_open_market.send_keys("Reliance")
        pre_open_market.click()

        """Большой sleep, чтобы страница точно успела подгузиться"""
        sleep(15)

        """Парсим таблицу"""
        soup = bs(driver.page_source, 'html.parser')
        table = soup.find('tbody').find_all('tr')

        driver.execute_script("window.scrollTo(0, 400);")

        for row in table:
            try:
                file_writer.writerow({"Наименование": row.find('a').text, "Цена": row.find('td', {'class': 'bold text-right'}).text})

            except Exception as e:
                print(e)
                continue
 
        sleep(4)

        """Переходим на HOME"""
        driver.delete_all_cookies()
        home_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main_navbar"]/ul/li[1]/a')))
        home_button.send_keys("Reliance")
        home_button.click()

        sleep(4)

        """Скроллим страницу вниз"""
        driver.delete_all_cookies()
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        sleep(2)

        """Перехоим на NSE Data&Analyst"""
        driver.delete_all_cookies()
        nse_data_analyst = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/footer/div/div[1]/div[2]/div/ul/li[3]/a')))
        nse_data_analyst.send_keys("Reliance")
        nse_data_analyst.click()

        sleep(3)

        """Скроллим страницу вниз"""
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        sleep(5)


    except Exception as e:
        print(e)
    finally:
        driver.delete_all_cookies()
        driver.close()
        driver.quit()


if __name__ == "__main__":
    nseindia_simulation(url)
