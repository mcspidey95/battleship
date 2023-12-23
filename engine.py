import random

class Ship:
    def __init__(self,size):
        self.row = random.randrange(0,9)
        self.col = random.randrange(0,9)
        self.size = size
        self.orient=random.choice(['h','v'])
        self.index = self.compute_index()

    def compute_index(self):
        start=self.row * 10 + self.col
        if self.orient == 'h':
            return [start + i for i in range(self.size)]
        elif self.orient == 'v':
            return [start + i*10 for i in range(self.size)]
        
class Player:
    def __init__(self):
        self.ships=[]
        self.search=['u' for i in range(100)]
        self.place_ships(sizes=[5,4,3,3,2])
        list_of_lists = [ship.index for ship in self.ships]
        self.index = [index for sublist in list_of_lists for index in sublist]
    
    def place_ships(self,sizes):
        for size in sizes:
            placed = False
            
            while not placed:
                ship=Ship(size)
                placement_possible = True
                
                for i in ship.index:
                    #ship must be in range
                    if i >= 100:
                        placement_possible = False
                        break
                    
                    #stop ship loop around
                    new_row = i//10
                    new_col = i%10
                    if new_row != ship.row and new_col != ship.col:
                        placement_possible = False
                        break
                    
                    #stop ship intersection
                    for other_ship in self.ships:
                        if i in other_ship.index:
                            placement_possible=False
                            break
                
                #placing ship
                if placement_possible:
                    self.ships.append(ship)
                    placed=True

    def show_ships(self):
        index = ['~' if i not in self.index else 'x' for i in range(100)]
        for row in range(10):
            print(" ".join(index[(row-1)*10:row*10]))


class Game:
    def __init__(self, human1, human2):
        self.human1 = human1
        self.human2 = human2
        self.player1 = Player()
        self.player2 = Player()
        self.player1_turn = True
        self.computer_turn = True if not self.human1 else False
        self.over = False
        self.result = None
        self.shots = 0

    def make_move(self, i):
        player = self.player1 if self.player1_turn else self.player2
        opponent = self.player2 if self.player1_turn else self.player1

        if i in opponent.index:
            player.search[i] = 'h'

            for ship in opponent.ships:
                sunk = True
                for i in ship.index:
                    if player.search[i]=='u':
                        sunk = False
                        break
                if sunk:
                    for i in ship.index:
                        player.search[i]='s'
        else:
            player.search[i] = 'm'

        game_over = True
        for i in opponent.index:
            if player.search[i]=='u':
                game_over = False
        self.over = game_over
        self.result = 1 if self.player1_turn else 2

        self.player1_turn = not self.player1_turn

        if (self.human1 and not self.human2) or (not self.human1 and self.human2):
            self.computer_turn = not self.computer_turn

        self.shots += 1
        
    def basic_ai(self):
        search = self.player1.search if self.player1_turn else self.player2.search
        unknown = [i for i, square in enumerate(search) if square =='u']
        hits = [i for i, square in enumerate(search) if square =='h']
        
        unknown_neigbors1 = []
        for u in unknown:
            if u+1 in hits or u-1 in hits or u-10 in hits or u+10 in hits:
                unknown_neigbors1.append(u)
        
        x = random.randint(1,2)
        if x==1:
            if len(unknown_neigbors1)>0:
                self.make_move(random.choice(unknown_neigbors1))
                return
        
        if len(unknown)>0:
            random_index = random.choice(unknown)
            self.make_move(random_index)

    def human_ai(self):
        mid = [33,35,44,46,53,55,64,66]
        search = self.player1.search if self.player1_turn else self.player2.search
        unknown = [i for i, square in enumerate(search) if square =='u']
        hits = [i for i, square in enumerate(search) if square =='h']
        
        #hit neigbour search
        unknown_neigbors1 = []
        unknown_neigbors2 = []
        for u in unknown:
            if u+1 in hits or u-1 in hits or u-10 in hits or u+10 in hits:
                unknown_neigbors1.append(u)
            if u+2 in hits or u-2 in hits or u-20 in hits or u+20 in hits:
                unknown_neigbors2.append(u)

        for u in unknown:
            if u in unknown_neigbors1 and u in unknown_neigbors2:
                self.make_move(u)
                return
        
        if len(unknown_neigbors1)>0:
            self.make_move(random.choice(unknown_neigbors1))
            return
        
        checker_board = []
        for u in unknown:
            row = u//10
            col = u%10
            if (row+col)%2==0:
                checker_board.append(u)
        
        for i in checker_board:
            if i in mid:
                self.make_move(i)
                return

        if len(checker_board)>0:
            self.make_move(random.choice(checker_board))
            return
        
        self.basic_ai()