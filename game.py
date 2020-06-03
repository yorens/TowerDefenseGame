from wave import Wave
from board import *
class Game:
    def __init__(self):
        # What this is doing, is that it is creating a board, multiple waves, appending them to the total list of waves, 
        # creating the list of path coordinates for the enemy to travel on, and creating the base.
        # The base is your base, you want to defend it from attacking enemies by placing towers down.
        # The very first time it asks you to place a tower it automaticalaly places one down for you otherwise you would
        # lose immediantly.
        self.board = Board(10, 10)
        self.waves = []
        # create_wave appends it to the list of waves
        self.create_wave([4, 9], 1, 25, 3, 1)
        self.create_wave([4, 9], 2, 45, 4, 2)
        self.create_wave([4, 9], 3, 50, 5, 3)
        self.create_wave([4, 9], 4, 65, 6, 4)
        self.create_wave([4, 9], 6, 75, 7, 5)
        self.create_wave([4, 9], 9, 80, 8, 6)
        self.create_wave([4, 9], 13, 85, 8, 7)
        self.create_wave([4, 9], 18, 90, 8, 8)
        self.create_wave([4, 9], 24, 95, 9, 9)
        self.create_wave([4, 9], 31, 99, 10, 10)
        # adding path in order
        self.board.add_path_in_order(Square(4,9, None, True))
        self.board.add_path_in_order(Square(5,9, None, True))
        self.board.add_path_in_order(Square(6,9, None, True))
        self.board.add_path_in_order(Square(6,8, None, True))
        self.board.add_path_in_order(Square(6,7, None, True))
        self.board.add_path_in_order(Square(6,6, None, True))
        self.board.add_path_in_order(Square(5,6, None, True))
        self.board.add_path_in_order(Square(4,6, None, True))
        self.board.add_path_in_order(Square(3,6, None, True))
        self.board.add_path_in_order(Square(3,5, None, True))
        self.board.add_path_in_order(Square(3,4, None, True))
        self.board.add_path_in_order(Square(3,3, None, True))
        self.board.add_path_in_order(Square(3,2, None, True))
        self.board.add_path_in_order(Square(3,1, None, True))
        # Create base
        self.board.set_square(Square(3,0, None, False, True))

    # creates wave with list of enemies.
    def create_wave(self, start_of_enemy_coords, enemy_damage, enemy_health, num_enemies, wave_number):
        w = Wave(wave_number)
        for i in range(num_enemies):
            i += 0
            w.add_enemy(Enemy(enemy_health, enemy_damage, 1, start_of_enemy_coords))
        self.waves.append(w)

    
    # This entire function is about placing a tower with having the coordinates not be ("blah", "yada"), but (5, 5).
    def tower_ask_v2(self, wave_number):
        int_ask = -1
        continue_asking = True
        while continue_asking:
            if wave_number == -1:
                ask = input("How many towers do you want to place? 0 or 1: ")
            elif wave_number > -1 and wave_number < 9:
                ask = input("How many towers do you want to place? 0, 1, or 2: ")
            elif wave_number >= 9:
                ask = input("How many towers do you want to place? 0, 1, 2, or 3: ")
            # The try/except checks whether they enter "blah" into a coordinate into a number.
            try:
                int_ask = int(ask)
                if wave_number == -1:
                    if int_ask > 1 or int_ask < 0:
                        continue
                elif wave_number > -1 and wave_number < 9:
                    if int_ask < 0 or int_ask > 2:
                        continue
                elif wave_number >= 9:
                    if int_ask < 0 or int_ask > 3:
                        continue
                continue_asking = False
            except ValueError:
                print("Please try again.")
        if int_ask > 0:
            for i in range(int_ask):
                i += 0
                continue_asking = True
                while continue_asking:
                    input_x = input("Please type in the x coordinate for your tower. ")
                    input_y = input("Please type in the y coordinate for your tower. ")
                    x = 0
                    y = 0
                    try:
                        # The next 5 lines check if the tower that you are placing is not a number, 
                        # on the path, on the base, and on another tower.
                        x = int(input_x)
                        y = int(input_y)
                        path_check = self.board.get_square(x, y).get_is_path()
                        base_check = self.board.get_square(x, y).get_is_base()
                        tower_check = self.board.get_square(x, y).get_tower() != None
                        if not path_check and not base_check and not tower_check:
                            self.board.get_towers().append(Towers(x, y, "archer", 5))
                            print("Ok.")
                            self.board.set_square(Square(x, y, Towers(x, y, "archer", 5), False))
                            continue_asking = False
                            break
                        else:
                            print("Sorry, you cannot place a tower there. Please try again.")

                    except ValueError:
                        print("This time enter an integer from 0 to " + str(self.board.get_x() - 1) + ".")
        # This else creates a tower in a random spot if you are just starting the game. If you are in later waves, 
        # this does not happen.
        else:
            if wave_number == -1:
                print("Ok. We will place one for you just because.")
                # This is here because we want to place a tower for them, so we randomize where we place it, but check if it is on the path, because towers cannot be on the path.
                j = random.randint(0, self.board.get_x())
                k = random.randint(0, self.board.get_y())
                if self.board.get_square(j, k).get_is_base() or self.board.get_square(j, k).get_is_path():
                    j = random.randint(0, self.board.get_x())
                    k = random.randint(0, self.board.get_y())
                elif self.board.get_square(j, k).get_is_base() == False or self.board.get_square(j, k).get_is_path() == False:
                    self.board.get_towers().append(Towers(j, k, "archer", 5))
                    self.board.set_square(Square(j, k, Towers(j, k, "archer", 5), False)) 
            else:
                print("Ok.")
            continue_asking = False

    # This makes every tower shoot once (if there's an enemy), gives the enemy a chance to move, 
    # gives the enemy a chance to attack the base, and starts a new wave if the last one is done.
    def do_1_turn(self):
        is_game_over = False
        # checking for a new wave
        if len(self.board.enemies) == 0:
            self.tower_ask_v2(self.board.wave_number)
            '''#wave speed
            wave_speed = int(input("What speed do you want the wave to be at (answer from 1-10. 7 is optimal speed, and smaller is faster)? "))
            while wave_speed < 1 or wave_speed > 10:
                wave_speed = int(input("What speed do you want the wave to be at (answer from 1-10. 7 is optimal speed, and smaller is faster)? "))
            wave_speed /= 10'''
            self.board.all_enemies = []
            for enemy in self.waves[0].wave_enemies:
                self.board.add_enemy(enemy)
            print("Starting wave " + str(self.waves[0].wave_number))
            self.board.wave_number = self.waves[0].wave_number
            del self.waves[0]
        # moving the enemies and making them attack the base if they can
        for e in self.board.get_enemies():
            old_x = e.location[0]
            old_y = e.location[1]
            new_x, new_y = e.move(self.board.get_ordered_path())
            if new_x == old_x and new_y == old_y:
                self.board.base_take_damage(e.damage)
        
        # making the towers shoot
        for tower in self.board.get_towers():
            if_enemy, damage, coords = tower.shoot(self.board.convert())
            coords = correct_coords(coords[0], coords[1], self.board.get_y())
            if if_enemy:
                for enemy in self.board.get_enemies():
                    if enemy.get_x() == coords[0] and enemy.get_y() == coords[1]:
                        enemy.health -= damage
                        if enemy.get_health() <= 0:
                            self.board.remove_enemy(enemy)
                        break
        # checks whether you won or lost
        if (len(self.waves) == 0 and len(self.board.enemies) == 0) or self.board.get_base_health() == 0:
            is_game_over = True
        #time.sleep(wave_speed)
        time.sleep(0.7)
        return is_game_over

    # starts a game.
    def start(self):
        self.board.max_wave_number = len(self.waves)
        self.board.display()
        while not self.do_1_turn():
            self.board.display()
            if len(self.board.enemies) == 0:
                print("Congratulations! Wave passed.")
        self.board.display()

# makes a game.
def main():
    game = Game()
    game.start()
    if game.board.get_base_health() > 0:
        print("Congratulations! You won! Game over.")
    else:
        print("GAME OVER. YOU LOSE.")

if __name__ == "__main__":
    main()







