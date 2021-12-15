import os
from time import sleep
from bs4 import BeautifulSoup as bs
from selenium import webdriver

"""Список прокси, нужно заполнить стабильными рабочими IP прокси"""
proxy_bank = [
#    '51.161.9.105:8080',
#    '51.161.9.105:8080'
]
url = 'https://twitter.com/elonmusk?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor'


def twitter_simulation(url):

    """Заполнение драйвера и его опций"""
    options = webdriver.ChromeOptions()
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
        """Заходим на twitter"""
        driver.get(url)

        sleep(5)
        driver.execute_script("window.scrollTo(0, 2000);")
        sleep(5)

        bsobj = bs(driver.page_source, 'html.parser')
        tweets = bsobj.find_all('div', {'class': 'css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu'})

        fw = open('tweets.txt', 'w', encoding='utf-8')

        for i in range(0,9):
            try:
                sleep(7)
                fw.write(str(i+1) + '{' + tweets[i].find('div', {'class': 'css-901oao r-18jsvk2 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0'}).find('span').text + '}')
                fw.write('\n')
                driver.get('https://twitter.com' + tweets[i].find('a', {'class': 'css-4rbku5 css-18t94o4 css-901oao r-14j79pv r-1loqt21 r-1q142lx r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-3s2u2q r-qvutc0'})['href'])                
                driver.execute_script("window.scrollTo(0, 1000);")
                sleep(5)
                sec_bs = bs(driver.page_source, 'html.parser')
                auths_list = sec_bs.find_all('a', {'class':'css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1wbh5a2 r-dnmrzs r-1ny4l3l'})
                for j in range(1,4):
                    fw.write('https://twitter.com' + auths_list[j]['href'])
                    fw.write('\n')
                
            except:
                continue

    except Exception as e:
        print(e)
    finally:
        fw.close()
        driver.delete_all_cookies()
        driver.close()
        driver.quit()


if __name__ == "__main__":
    twitter_simulation(url)
