import numpy as np

def get_score(row, dices):
    if row==1:
        return np.sum(dices==1) * 1
    elif row==2:
        return np.sum(dices==2) * 2
    elif row==3:
        return np.sum(dices==3) * 3
    elif row==4:
        return np.sum(dices==4) * 4
    elif row==5:
        return np.sum(dices==5) * 5
    elif row==6:
        return np.sum(dices==6) * 6
    elif row==7: # total
        return np.sum(dices)
    elif row==8: # 4 of a kind
        return max([(np.sum(dices==x)>=4)*np.sum(dices) for x in range(1,7)])
    elif row==9: # full-house
        s_dice = sorted(dices)
        is_full_house = s_dice[0]==s_dice[1] and s_dice[3]==s_dice[4] and \
                (s_dice[2]==s_dice[0] or s_dice[2]==s_dice[4])
        return np.sum(dices) if is_full_house else 0
    elif row==10: # Sm. Straight
        cond1 = 1 in dices and 2 in dices and 3 in dices and 4 in dices
        cond2 = 2 in dices and 3 in dices and 4 in dices and 5 in dices
        cond3 = 3 in dices and 4 in dices and 5 in dices and 6 in dices
        if cond1 or cond2 or cond3:
            is_sm_straight = True
        else:
            is_sm_straight = False
        return 15 if is_sm_straight else 0
    elif row==11: # Lg. Straight
        s_dice = np.array(sorted(dices))
        if 2 in dices and 3 in dices and 4 in dices and 5 in dices and (1 in dices or 6 in dices):
            is_lg_straight = True
        else:
            is_lg_straight = False
        return 30 if is_lg_straight else 0
    elif row==12: # Yachtzee
        is_yachtzee = dices[0]==dices[1] and dices[0]==dices[2] and dices[0]==dices[3] and dices[0]==dices[4]
        return 50 if is_yachtzee else 0
    raise ValueError("Invalid action. No such action: "+str(row)+".")

def get_total_score(_table):
    _table_clip = np.clip(_table, 0, 100)
    score6 = np.sum(_table_clip[:6])
    _bonus = 35 if score6>=63 else 0
    _total = np.sum(_table_clip)
    return _total+_bonus, (score6, _bonus)

def Yachtzee_step(state=None, action=None):
    if state is None:
        _table = -np.ones(12, int)
        _dices = (np.random.random(5)*6+1).astype(int)
        _round = 2
    else:
        assert action is not None
        _table, _dices, _round = state
        _dice_stay, _row = action
        if _row>12:
            raise ValueError("Invalid action. No such action: "+str(_row)+".")
        elif _row>0:
            if _table[_row-1]>=0:
                raise ValueError("Invalid action. Row "+str(_row)+" is occupied.")
            _table[_row-1] = get_score(_row, _dices)
            valid_rows = [i for i,x in enumerate(_table) if x<0]
            if len(valid_rows)==0:
                return _table, None, None
            else:
                _dices = (np.random.random(5)*6+1).astype(int)
                _round = 2
        else:
            if _round<=0:
                raise ValueError("Invalid action. Cannot re-roll the dice.")
            new_dices = (np.random.random(5)*6+1).astype(int)
            _dices = (_dices * _dice_stay + new_dices * (1-_dice_stay)).astype(int)
            _round-=1
    return [_table, _dices, _round]

def print_table(_table):
    row_names = [
        "Aces", "Deuces", "Threes", "Fours", "Fives", "Sixes",
        "Chance", "4 of a kind", "Full House", "Sm. Straight", "Lg. Straight", "Yachtzee"
    ]
    total_score, (score6, bonus) = get_total_score(_table)
    for i in range(6):
        print("row "+str(i+1)+"  "+row_names[i]+":", _table[i])
    print("Bonus:", bonus, "("+str(score6)+"/63)")
    for i in range(6,9):
        print("row "+str(i+1)+"  "+row_names[i]+":", _table[i])
    for i in range(9,12):
        print("row "+str(i+1)+" "+row_names[i]+":", _table[i])
    print("Total:", total_score)

class Game:
    """
    state:
        [_table, _dices, _round]
        _table:
            [1, -1, -1, 12, 16, -1, 25, 24, 15, 30, 22, 0] # results of each row, -1 for not occupied
        _dices:
            [4, 1, 6, 6, 6] # current dices
        _round:
            2 # number of re-roll left
    action:
        [_dice_stay, _row]
        _dice_stay:
            [0, 0, 1, 1, 1], #1 for stay and 0 for re-roll
        _row:
            3 # 0 for re-roll, others for put the number into which row
    """
    
    def __init__(self):
        self.state = Yachtzee_step(state=None, action=None)
        self.is_finished = False
    
    def get_valid_actions(self):
        if self.is_finished:
            return [0 for _ in range(len(self.state[0])+1)]
        else:
            return [1 if self.state[2]>0 else 0]+[1 if x<0 else 0 for x in self.state[0]]
    
    def take_action(self, action):
        print(action)
        self.state = Yachtzee_step(self.state, action)
        if self.state[2] is None:
            self.is_finished = True
    
    def show(self):
        print_table(self.state[0])