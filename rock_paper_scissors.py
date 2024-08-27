from random import randint

class Turn:
    '''
    Ход

    Содержит поля:
    side - ходящая сторона (1 - компьютер, 2 - человек)
    choice - выбор ('к' - камень, 'н' - ножницы, 'б' - бумага)
    '''
    
    def __init__(self, side: int, choice: str):
        '''
        Конструктор

        :param side: ходящая сторона (1 - компьютер, 2 - человек)
        :type side: int
        :param choice: выбор ('к' - камень, 'н' - ножницы, 'б' - бумага)
        :type choice: str
        '''

        self.side = side
        self.choice = choice

class GameSeria:
    '''
    Серия игр

    Содержит поля:
    user_win - статистика, сколько игр выиграл пользователь
    comp_win - сколько игр выиграл компьютер
    n_turns - общее количество заказанных игр
    dic_human_turns - количество ходов каждого вида, выбранных пользователем
    dic_comp_turns - количество ходов каждого вида, выбранных компьютером
    '''

    CHOICE_POSSIBLE = ('к', 'н', 'б')
    COMP_SIDE = 1
    HUMAN_SIDE = 2
    
    def __init__(self, n_turns: int):
        '''
        Конструктор

        :param n_turns: количество заказанных игр
        :type n_turn: int
        '''

        self.user_win = 0
        self.comp_win = 0
        self.n_turns = n_turns
        self.dic_human_turns = {
            'к': 0,
            'н': 0,
            'б': 0
        }
        self.dic_comp_turns = {
            'к': 0,
            'н': 0,
            'б': 0
        }

    def choose_comp_turn(self) -> Turn:
        '''
        Компьютерный ход
        '''
        choice = GameSeria.CHOICE_POSSIBLE[randint(0, len(GameSeria.CHOICE_POSSIBLE) - 1)]
        return Turn(GameSeria.COMP_SIDE, choice)
    
    def choose_human_turn(self) -> Turn:
        '''
        Ход пользователя
        '''
        while True:
            choice = input('Делай ход, кожаный! (к, н, б)')
            if choice in GameSeria.CHOICE_POSSIBLE:
                return Turn(GameSeria.HUMAN_SIDE, choice)
            else:
                print('Так не ходят!')

    def fill_stat(self, turn: Turn):
        '''
        Учитываем ход в статистике

        :param turn: ход
        :type turn: Turn
        '''
        if turn.side == GameSeria.COMP_SIDE:
            dic = self.dic_comp_turns
        else:
            dic = self.dic_human_turns

        dic[turn.choice] += 1

    def who_is_winner(self, turn1: Turn, turn2: Turn) -> int:
        '''
        Определение победителя

        Если выдало 0, то ничья
        '''
        match turn1.choice:
            case 'к':
                match turn2.choice:
                    case 'н': return turn1.side
                    case 'б': return turn2.side
                    case _: return 0
            case 'н':
                match turn2.choice:
                    case 'к': return turn2.side
                    case 'б': return turn1.side
                    case _: return 0
            case 'б':
                match turn2.choice:
                    case 'к': return turn1.side
                    case 'н': return turn2.side
                    case _: return 0
            case _: return 0

    def turn(self):
        '''
        Ход
        '''
        turn_comp = self.choose_comp_turn()
        turn_human = self.choose_human_turn()

        self.fill_stat(turn_comp)
        self.fill_stat(turn_human)

        print(f'А у меня {turn_comp.choice}.')
        winner = self.who_is_winner(turn_comp, turn_human)

        match winner:
            case GameSeria.COMP_SIDE: 
                print('Я выиграл, муаххахаха!')
                self.comp_win += 1
            case GameSeria.HUMAN_SIDE: 
                print('Оппа, ты выиграл!')
                self.user_win += 1
            case _: print('Хе, ничья, однако!')

    def play(self):
        '''
        Серия игр
        '''
        for _ in range(self.n_turns):
            self.turn()

        print(f'Ты выиграл {self.user_win} раз, а я {self.comp_win} раз')
        print(f'Ты выбрал камень {self.dic_human_turns['к']} раз, а я {self.dic_comp_turns['к']} раз')
        print(f'Ты выбрал ножницы {self.dic_human_turns['н']} раз, а я {self.dic_comp_turns['н']} раз')
        print(f'Ты выбрал бумагу {self.dic_human_turns['б']} раз, а я  {self.dic_comp_turns['б']} раз')

def main():
    '''
    Запускатор
    '''
    gameSeria = GameSeria(15)
    gameSeria.play()

if __name__ == '__main__':
    main()