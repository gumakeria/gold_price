from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time
from datetime import datetime

urls = {
    "XAU/USD": "https://www.investing.com/currencies/xau-usd-historical-data",
}

def get_price(link):
    grid_url = "http://selenium-hub:4444/wd/hub"
    
    chrome_options = Options()
    chrome_options.add_argument('--disable-dev-shm-usage') 
    chrome_options.add_argument('--blink-settings=imagesEnabled=false') # ko load anh
    
    #Wait
    #wait = WebDriverWait(driver,15)


    driver = webdriver.Remote(command_executor=grid_url, options=chrome_options)
    driver.get(link)
    time.sleep(5)
    
    price_elements = driver.find_elements(By.CLASS_NAME, "historical-data-v2_price__atUfP")
    if price_elements:
        price = price_elements[0].text.replace(' ', '##')
    else:
        price = ""
    driver.quit()
    return price

if __name__ =='__main__':
    prices = {}
    for currency, link in urls.items():
        prices[currency] = get_price(link)

    if prices:
        data_str = list(prices.values())[0]
        data_list = data_str.split('##')
        data_list[-1] = data_list[-1].replace('%', '')
        for i in range(1, 5):
            data_list[i] = data_list[i].replace(',', '')
 
        # Chuyển đổi ngày tháng
        date_str = data_list[0]
        date_obj = datetime.strptime(date_str, '%m/%d/%Y')
        formatted_date_str = date_obj.strftime('%Y-%m-%d %H:%M:%S')
        data_list[0] = formatted_date_str

        with open('data_insert.txt', 'w') as file:
            for item in data_list:
                file.write(f"{item}\n")

    print("ok")
