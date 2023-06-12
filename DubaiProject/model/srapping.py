from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
import os

def collect_dubai_properties_info(driver):

    cards = driver.find_elements(By.CLASS_NAME,"card_title")
    card_text = [card.text for card in cards]
    card_text = [card.split('\n')[1] for card in card_text]

    prices = driver.find_elements(By.CLASS_NAME,"price")
    prices_text = [price.text for price in prices]

    about_tour = driver.find_elements(By.CLASS_NAME,"about_tour")
    about_tour_info = [tour_info.text for tour_info in about_tour]
    bedroom = [tour.split('\n')[0] for tour in about_tour_info]
    square = [tour.split('\n')[2] if len(tour.split('\n'))==3 else 1 for tour in about_tour_info]
    bathroom = [tour.split('\n')[1] for tour in about_tour_info]
        
    dict_for_df = {
            'district' : card_text,
            'bedroom' : bedroom,
            'bathroom' : bathroom,
            'square' : square,
            'price' : prices_text
    }
    driver.implicitly_wait(10)
        #element = driver.find_element(By.XPATH,f'/html/body/div[1]/div[5]/div/div/a[{str(page)}]')
        #driver.execute_script("arguments[0].click();", element)
        #time.sleep(50)
    
    return dict_for_df

def get_html_page(value):

    options = Options()
    options.add_argument(argument='--allow-running-insecure-content')
    options.add_argument(argument='--ignore-certificate-errors')
    options.add_argument(argument='--ignore-ssl-errors')
    options.add_argument("log-level=3")

    service = Service("C:\chromedriver.exe")
    driver = webdriver.Chrome(service=service,options=options)
    driver.set_window_size(1920,1080)
    
    if value in [0,1]:
        driver.get("https://www.allsoppandallsopp.com/dubai/properties/residential/lettings/propertytype-apartment")
    else:
        driver.get(f"https://www.allsoppandallsopp.com/dubai/properties/residential/lettings/propertytype-apartment/page-{str(value)}")

    result = collect_dubai_properties_info(driver)
    
    driver.implicitly_wait(10)
    driver.close()
    print(f'Page {value} Collected')
    return result

def main():
    
    dict_results = []
    for i in range(1,27):
        dict_results.append(get_html_page(i))
    update_json_file(dict_results)

def create_json_file(dict_results):
    
    with open('dubai_properties.json', 'w') as file:
            json.dump(dict_results,file,indent=2)
        
def update_json_file(dict_results):
    
    path = r'DubaiProject\model\dubai_properties.json'
    if os.path.exists(path):
        os.remove(path)
        create_json_file(dict_results)
    else:
        create_json_file(dict_results)

if __name__ == "__main__":
    
    '''thr_info = []
    for i in range(1,27):
        thread = threading.Thread(target=main, args=(i,), name=f'page-{i}')
        thr_info.append(thread)
        thread.start()
    for i in thr_info:
        i.join()'''
            
    print("Scapping starts")
    main()
    print('Json is ready')