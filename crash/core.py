from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import time
import datetime

def main():
    match_number = 0

    with open('output.csv', 'w') as f:
        f.write('date,time,match_number,crashNumber,players,max_bet,min_bet,total bet,total_profit\n')

    navegador = webdriver.Firefox()
    try:

        navegador.get('https://www.gamdom.com')
        ui.WebDriverWait(navegador, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'icon-crash')))
        navegador.find_element_by_class_name('icon-crash').click()

        progress = False
        while True:
            status = get_status_game(navegador)

            if (status == 'Inprogress | Good Luck' and progress == False):
                print('[Game in progress]')
                time.sleep(0.75)
                date, hour = get_time()
                print('Date {} - {}\n' .format(date, hour))
                players, bet, max_bet, min_bet = crawl_info_from_game(navegador)
                print('{} players. Total bet: {}\n'.format(players, bet))
                progress = True

            if ('Crashed' in status and progress == True):
                match_number += 1
                progress = False
                total_profit = get_after_game_status(navegador)

                crashNumber = status.split('@')[1].strip().replace('x', '')
                print('[Game Crashed] {}\n'.format(crashNumber))

                output = "{},{},{},{},{},{},{},{},{}".format(date, hour, match_number, crashNumber, players, max_bet, min_bet, bet, total_profit)
                write_row(output)

    except Exception as e:
        navegador.quit()
        raise e

def write_row(data):
    with open('output.csv', 'a') as f:
        f.write(data + '\n')

def get_status_game(navegador):
    return navegador.find_element_by_class_name('pro_txt').get_attribute('innerHTML').strip()

def get_time():
    full_date = str(datetime.datetime.now())
    date = full_date.split(' ')[0]
    hour = full_date.split(' ')[1].split('.')[0]

    return date, hour

def crawl_info_from_game(navegador):
    ui.WebDriverWait(navegador, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'pl_onli')))
    players = navegador.find_elements_by_class_name('pl_onli')[0].get_attribute('innerHTML')
    total_bet = navegador.find_elements_by_class_name('pl_onli')[1].find_element_by_tag_name('span').get_attribute('innerHTML')
    total_bet = total_bet.replace('\u202f','')

    table = navegador.find_element_by_class_name('pl_table_data')
    profit_html = table.find_elements_by_class_name('pl_bet')
    array_bet = []

    for single_profit_html in profit_html:
        array_bet.append(int(single_profit_html.get_attribute('innerHTML').replace('\u202f','')))

    return players, total_bet, np.max(array_bet), np.min(array_bet)

def get_after_game_status(navegador):
    table = navegador.find_element_by_class_name('pl_table_data')
    profit_html = table.find_elements_by_class_name('pl_profit')
    array_profit = []

    for single_profit_html in profit_html:
        array_profit.append(int(single_profit_html.get_attribute('innerHTML').replace('\u202f','')))

    return np.sum(array_profit)

if __name__ == "__main__":
    main()