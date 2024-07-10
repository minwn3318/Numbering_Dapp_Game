import random

def Rankig_Game():
    playGame = True
    print("+----------------+")
    print("+ Numbering Game +")
    print("+----------------+ \n")
    while(playGame) :
        print("(1)input 'S' to start Game\n(2) input 'M', show manual\n(3)input 'R', show Ranking\n(4) input 'Q', exit game\n")
        input_key = input(": ")
        if input_key == "S" :
            difficult_loop = True
            ranking_data = {
                    "Difficalty" : None,
                    "Name" : None,
                    "Number" : None,
                    "Try" : None,
                }
            number = None

            while(difficult_loop) :
                print("select difficalt name\n(1) easy - (0 ~ 100), (2) nomal - (0 ~ 500), (3) hard - (0~1000)")
                difficult = input(": ")
                ranking_data["Difficalty"] = difficult
                if difficult != "easy" and difficult != "nomal" and difficult != "hard" :
                    print("please input again")
                else :
                    max = None
                    if difficult == "easy" :
                        max = 100
                    elif difficult == "nomal" :
                        max = 500
                    else :
                        max = 1000
                    number = random.randint(0,max)
                    print(number)
                    ranking_data["Number"] = number
                    difficult_loop = False

            print("put your name")
            user_name = input(": ")
            ranking_data["Name"] = user_name
            print(ranking_data)
            difficult_loop = True

            count = 1
            while(True):
                print("Guess Numger! :")
                guess = int(input())
                if guess == ranking_data["Number"] :
                    print("correct!!")
                    print(count)
                    ranking_data["Try"] = count
                    count = 0
                    break
                elif guess < ranking_data["Number"] :
                    print("UP!!")
                else  :
                    print("Down!!")
                count = count + 1
            print(ranking_data)

        elif input_key == "M" :
            print("+----------------+")
            print("+     manual     +")
            print("+----------------+ \n")
        elif input_key == "R" :
            print("+----------------+")
            print("+     ranking    +")
            print("+----------------+ \n")
        elif input_key == "Q" :
            print("+----------------+")
            print("+    exit Game   +")
            print("+----------------+ \n")
            playGame = False

Rankig_Game()