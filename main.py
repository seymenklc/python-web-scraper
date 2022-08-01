from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

data = []
stops = []
departure_times = []
arrival_times = []

def app_driver():
    url = "https://www.izban.com.tr/Sayfalar/SeferSaatleri.aspx?MenuId=22"
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    return driver

def get_stops(all_stops):
    # get each individual stop name
    for stop in all_stops.find_elements(By.TAG_NAME, 'option'):
        stops.append(stop.text)
    return stops

def get_data(table):
    for row in table.find_elements(By.TAG_NAME, "tr"):
        data.append(row.text) 
    return data

def split_times(times):  
    for time in times: 
        departure_times.append(time.split()[0])
        arrival_times.append(time.split()[1])
    return departure_times, arrival_times

def get_titles():
    return data[slice(3)]
    
def main():    
    driver = app_driver()
    movement_stop_dd = driver.find_element(By.ID, 'ctl00_CPH_drpHareketDur')
    sleep(1)
    get_stops(movement_stop_dd)
    movement_station_select = Select(movement_stop_dd)
    movement_station_select.select_by_visible_text('Menemen') 
    sleep(1)
    arrival_stop_dd = driver.find_element(By.ID, "ctl00_CPH_drpVarisDur")
    arrival_stop_select = Select(arrival_stop_dd)
    arrival_stop_select.select_by_visible_text('Alsancak')
    sleep(1)
    driver.find_element(By.ID, "ctl00_CPH_Goster").click()
    sleep(1)
    table = driver.find_element(By.TAG_NAME, "table")
    get_data(table)
    sleep(1)
    get_titles()
    split_times(data[slice(4, len(data)-1+1)])
    
    driver.quit()
       
main()