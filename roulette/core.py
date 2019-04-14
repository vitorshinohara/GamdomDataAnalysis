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
        f.write('match_number,date,hour,value,total_bet_red,total_bet_green,total_bet_black,total_bet\n')

    navegador = webdriver.Firefox()
    try:

        navegador.get('https://www.gamdom.com/roulette')

        progress = False
        while True:
            status = get_status_game(navegador)           

            if (status == 'RODANDO | BOA SORTE!' and progress == False):
                print('[Game in progress]')
                time.sleep(0.75)
                date, hour = get_time()
                print('[{} - {}] ' .format(date, hour))
                total_bet_red,total_bet_green,total_bet_black,total_bet = crawl_info_from_game(navegador)
                progress = True

            if (status != 'RODANDO' and status != 'RODANDO | BOA SORTE!' and progress == True):
                match_number += 1
                progress = False
                value,color = get_after_game_status(navegador)
                print('[Result: {} - {} ]\n'.format(value,color))

                output = "{},{},{},{},{},{},{},{}".format(match_number,date,hour,value,total_bet_red,total_bet_green,total_bet_black,total_bet)
                write_row(output)

    except Exception as e:
        navegador.quit()
        raise e

def write_row(data):
    with open('output.csv', 'a') as f:
        f.write(data + '\n')

def get_status_game(navegador):
    try:
        status = navegador.find_element_by_css_selector('.pro_txt').get_attribute('innerText')
    except Exception as identifier:
        status = navegador.find_element_by_css_selector('.game_progress').get_attribute('innerText')

    return status

def get_time():
    full_date = str(datetime.datetime.now())
    date = full_date.split(' ')[0]
    hour = full_date.split(' ')[1].split('.')[0]

    return date, hour

def crawl_info_from_game(navegador):    
    total_bet_red = navegador.find_element_by_css_selector('div.row:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > span:nth-child(2) > span:nth-child(1)').get_attribute('innerText')
    total_bet_green = navegador.find_element_by_css_selector('div.row:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > span:nth-child(2) > span:nth-child(1)').get_attribute('innerText')
    total_bet_black = navegador.find_element_by_css_selector('div.row:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > span:nth-child(2) > span:nth-child(1)').get_attribute('innerText')
    
    total_bet_black = ''.join(total_bet_black.split())
    total_bet_green = ''.join(total_bet_green.split())
    total_bet_red = ''.join(total_bet_red.split())
    
    print(total_bet_black)
    print(total_bet_green)
    print(total_bet_red)
    
    total_bet = int(total_bet_red) + int(total_bet_green) + int(total_bet_black)

    return total_bet_red,total_bet_green,total_bet_black,total_bet


def get_after_game_status(navegador):
    value = int(navegador.find_element_by_css_selector('.game_progress').get_attribute('innerText'))
    if (value > 0 and value < 8):
        color = "red"
    elif (value > 7):
        color = "black"
    else:
        color = "green"

    return value,color

if __name__ == "__main__":
    main()