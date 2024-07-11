import random
import pygame
import sys
import requests
import json
import pandas as pd
import sqlite3

pygame.init()

def return_key():
    for event in pygame.event.get() :
        return event

def making_RankingData():
    ranking_data = {
            "Difficalty" : None,
            "Name" : None,
            "Number" : None,
            "Try" : None,
        }
    return ranking_data

def select_Difficulty(ranking_data, event) :
    max = None
    difficult = None

    if event.key == pygame.K_1 :
        difficult == "easy"
        max = 100
    elif event.key == pygame.K_2:
        difficult == "nomal" 
        max = 500
    elif event.key == pygame.K_3 :
        difficult == "nomal" 
        max = 1000

    if difficult != None and max != None :
        number = random.randint(0,max)
        ranking_data["Number"] = number
        return ranking_data

def input_UserName(ranking_data, event, str_name) :
    if event.unicode.isalpha():
        str_name = str_name + event.unicode
    elif event.key == pygame.K_KP_ENTER or event == pygame.KSCAN_KP_ENTER :
        ranking_data["Name"] = str_name
        return ranking_data

def playing_Game(ranking_data, event, number, count) :
    if event.unicode.isdigit():
        number = number + event.unicode

    if event.key == pygame.K_KP_ENTER or event == pygame.KSCAN_KP_ENTER :
        if number == ranking_data["Number"] :
            print("correct!!")
            print(count)
            ranking_data["Try"] = count
            count = 0
            return ranking_data

        else :
            if number < ranking_data["Number"] :
                print("UP!!")
            else  :
                print("Down!!")

            number = ""
            count = count + 1

def transmit_rankingTransaction(ranking_data) :
    data = {
            "sender": "user",
            "recipient": "user",
            "amount": 0,
            "smart_contract" : {
                "ranking" : ranking_data
            }   
        }
    headers = {'Content-Type' : 'application/json; charset=utf-8'}
    requests.post("http://127.0.0.1:5000/transactions/new", headers=headers, data=json.dumps(data))

type_ranking = []
easy_ranking = None
nomal_ranking = None
hard_ranking = None

def show_ranking() :
    headers = {'Content-Type' : 'application/json; charset=utf-8'}
    value = requests.get("http://127.0.0.1:5000/chain", headers=headers)
    for transaction in value :
        if "ranking" in transaction :
            type_ranking.append(transaction["smart_contract"]["ranking"]) 
    
    conn = sqlite3.connect('sample.db')
    ranking_Frame = pd.DataFrame(type_ranking)

    ranking_Frame.to_sql('ranking_list',conn)

    easy_ranking = pd.read_sql_query("SELECT Difficalty, Name, Number, Try FROM ranking_list Where Difficalty = easy ORDER BY Try DESC LIMIT 10", conn)
    nomal_ranking = pd.read_sql_query("SELECT Difficalty, Name, Number, Try FROM ranking_list Where Difficalty = easy ORDER BY Try DESC LIMIT 10", conn)
    hard_ranking = pd.read_sql_query("SELECT Difficalty, Name, Number, Try FROM ranking_list Where Difficalty = easy ORDER BY Try DESC LIMIT 10", conn)
    
    print(easy_ranking)
    print(nomal_ranking)
    print(hard_ranking)


def show_Manual():
    print("\n게임설명 :\n숫자 범위에서 무작위로 선정된 숫자를 맞추면 이기는 게임입니다\n\n게임플레이방법 : \n(1) 먼저 난이도를 선택합니다\n(2) 선택한 난이도에 맞는 숫자 범위에서 무작위 숫자가 선택됩니다\n(3) 화면의 빈칸에 숫자를 입력하면 되며, 시스템은 입력한 숫자가 실제 숫자보다 작다면 up, 실제 숫자보다 크다면 down을 외칩니다.\n(4) 플레이어는 그에 맞게 다시 숫자를 조정하여 입력하면 됩니다.\n(5) 게임이 끝나게 되면 난이도, 플레이어의 이름, 숫자, 시도횟수가 출력된 후 최종적인 랭킹에 입력되고 랭킹화면을 보여주며 게임을 종료합니다")

drawing_state = ["ready", "manual", "level", "name", "play", "ranking"]
state = None
