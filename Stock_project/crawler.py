from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import openpyxl

def get_code(request):
    df = pd.read_html('상장법인목록.xls')[0]
    df['종목코드'] = df['종목코드'].map('{:06d}'.format)
    excel_file = openpyxl.Workbook()
    sheet = excel_file.active
    excel_file.save('ref_company.xlsx')
    df.to_excel('ref_company.xlsx', index = False)
    excel_file.close()
    excel = 'ref_company.xlsx'
    data = pd.read_excel(excel, sheet_name='Sheet1')
    company_code = ''
    data_dict = {}
    for item in data.itertuples():
        data_dict[item[1]] = item[2]
    for dt in data_dict:
        if request == dt:
            company_code = '{:06d}'.format(data_dict[dt])
    return company_code
                
def get_sise(company_code):
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    BASE_URL = 'https://finance.naver.com/item/main.naver?'
    # driver = webdriver.Chrome('/home/ubuntu/.local/bin/chromedriver.exe')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options = options)
    parameters = 'code=' + str(company_code)
    url = BASE_URL + parameters
    driver.get(url)
    sise_btn = driver.find_element(By.CSS_SELECTOR, '.tabs_submenu  li .tab2')
    sise_btn.click()
    sise_frame = driver.find_elements(By.CSS_SELECTOR, 'iframe[name = day]')
    SISE_DAY_URL = sise_frame[1].get_attribute('src')
    sise_day_url = SISE_DAY_URL
    driver.get(sise_day_url)
    sise_data = driver.find_elements(By.CSS_SELECTOR, 'tbody tr')
    date_collection = []; closing_collection = []; difference_collection = []; opening_collection = []
    highest_collection = []; lowest_collection = []; quantity_collection = []
    for sise in sise_data[1:15]:
        try:
            if len(sise.text.split(' ')[0]) != 0:
                    date_collection.append(sise.text.split(' ')[0])
                    closing_collection.append(sise.text.split(' ')[1])
                    difference_collection.append(sise.text.split(' ')[2])
                    opening_collection.append(sise.text.split(' ')[3])
                    highest_collection.append(sise.text.split(' ')[4])
                    lowest_collection.append(sise.text.split(' ')[5])
                    quantity_collection.append(sise.text.split(' ')[6])
        except: pass
        sise_data_dict = {'날짜': date_collection, '종가': closing_collection, '전일비': difference_collection, '시가': opening_collection, 
                        '고가': highest_collection, '저가': lowest_collection, '수량': quantity_collection}
    idx = [num for num in range(1, len(date_collection)+1)]
    sise_data_table = pd.DataFrame(sise_data_dict, index = idx)
    driver.quit()
    return sise_data_table
         
def get_news(company_code):
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    # driver = webdriver.Chrome('/home/ubuntu/.local/bin/chromedriver.exe')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options = options)
    BASE_URL = 'https://finance.naver.com/item/main.naver?'
    parameters = 'code=' + str(company_code) 
    url = BASE_URL + parameters
    driver.get(url)
    news_btn = driver.find_element(By.CSS_SELECTOR, '.tabs_submenu  li .tab5')
    news_btn.click()
    NEWS_URL = 'https://finance.naver.com'
    parameters = '/item/news_news.naver?code=' + str(company_code) +'&page=&sm=title_entity_id.basic&clusterId='
    news_url = NEWS_URL + parameters
    driver.get(news_url)
    news_title = driver.find_elements(By.CSS_SELECTOR, 'tr .title > a')
    news_press = driver.find_elements(By.CSS_SELECTOR, 'tr .info')
    news_date = driver.find_elements(By.CSS_SELECTOR, 'tr .date')
    title_collection = []; url_collection = []; press_collection = []; date_collection = []
    for news in news_title:
        if news.text.strip() != '':
            title_collection.append(news.text)
            urls = news.get_attribute('href')
            url_collection.append(urls)
    for news in news_press:
        if news.text.strip() != '':
            press_collection.append(news.text)
    for news in news_date:
        if news.text.strip() != '':
            date_collection.append(news.text)
    news_data_dict = {'제목': title_collection, 'url': url_collection, '언론사': press_collection, '날짜': date_collection}
    idx = [num for num in range(1, len(title_collection)+1)]
    news_data_table = pd.DataFrame(news_data_dict, index = idx)
    driver.quit()
    return news_data_table