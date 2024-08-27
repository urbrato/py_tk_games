import random
computer = 'камень', 'ножницы', 'бумага'
n = int(input())
player_win = 0
PC_win = 0
stonePlayer = 0
stonePC = 0
scissorsPlayer = 0
scissorsPC = 0
paperPlayer = 0
paperPC = 0
for i in range(n):
    player = int(input('камень(1), ножницы(2) или бумага(3)?'))

    PC_choise = random.randint(0, 2)
    print(f' компьютер выбрал {computer[PC_choise]}')
    if PC_choise == player - 1:
        print('ничья')
    else:
        if PC_choise == 0:
            if player == 2:
                print('компьютер выиграл')
                PC_win += 1
                stonePC += 1
            elif player == 3:
                print('вы выиграли')
                player_win += 1
                paperPlayer += 1
        elif PC_choise == 1:
            if player == 1:
                print('вы выиграли')
                player_win += 1
                stonePlayer += 1
            elif player == 3:
                print('компьютер выиграл')
                PC_win += 1
                scissorsPC += 1
        else:
            if player == 1:
                print('компьютер выиграл')
                PC_win += 1
                paperPC += 1
            elif player == 2:
                print('вы выиграли')
                player_win += 1
                scissorsPlayer += 1
print(f'вы выиграли {player_win} раз')
print(f'компьютер выиграл {PC_win} раз')