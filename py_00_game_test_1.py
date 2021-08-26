import numpy as np

from game_env.env import Game

def get_inputs(valid_rows, _round):
    is_input_valid = False
    while not is_input_valid:
        indices_str = input("Please type the indices of dices you want to keep (e.g. 0,2,3), or 'r' + the row of the table if you do not want to re-roll the dice (e.g. r7): ")
        if len(indices_str)==0:
            if _round<=0:
                print("Invalid input: No re-roll left.")
                continue
            return False, []
        
        if indices_str[0]=='r':
            is_row = True
            try:
                indices = int(indices_str[1:])
                if indices-1 not in valid_rows:
                    print("Invalid input.")
                    continue
            except:
                print("Invalid input.")
                continue
        else:
            if _round<=0:
                print("Invalid input: No re-roll left.")
                continue
            is_row = False
            try:
                indices = sorted(list(set([int(x.strip()) for x in indices_str.split(",") if len(x)>0])))
                if indices[-1]>4 or indices[0]<0:
                    print("Invalid input.")
                    continue
            except:
                print("Invalid input.")
                continue
        is_input_valid = True
    return is_row, indices

if __name__=="__main__":
    game = Game()
    game.show()
    _table, _dices, _round = game.state
    valid_rows = [i for i,x in enumerate(_table) if x<0]
    while _round is not None:
        print()
        print("        0 1 2 3 4")
        print("Dices:", _dices, "   Re-roll:", _round)
        print(game.get_valid_actions())
        
        is_row, indices = get_inputs(valid_rows, _round)
        if is_row:
            action = None, indices
        else:
            _dice_stay = np.zeros(5)
            _dice_stay[indices] = 1
            action = _dice_stay, 0
            
        game.take_action(action)
        game.show()
        _table, _dices, _round = game.state
        valid_rows = [i for i,x in enumerate(_table) if x<0]