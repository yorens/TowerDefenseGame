from enemies import Enemy
from towers import Towers
import random
import time

random.seed()

# Inside the array of arrays of objects (the game board), the objects are Squares.
# Inside each square, it has coordinates, an x and a y, 2 NoneTypes which are enemy
# and tower, is_path which is either True or False, and is_base, which is automatically set to 
# False unless you set it to True.
class Square:
    def __init__(self, x, y, tower, is_path, is_base = False):
        self.tower = tower
        self.x = x
        self.y = y
        self.is_path = is_path
        self.is_base = is_base

    def get_tower(self):
        return self.tower

    def set_tower(self, tower):
        self.tower = tower

    def get_terrain(self):
        if self.is_base:
            return "b"
        elif self.tower != None:
            return self.tower.get_tower_type()
        elif self.is_path:
            return "X"
        return "-"

    def get_x(self):
        return self.x

    def set_x(self, x):
        self.x = x

    def get_y(self):
        return self.y

    def set_y(self, y):
        self.y = y

    def get_is_base(self):
        return self.is_base

    def get_is_path(self):
        return self.is_path

    # The line functions are for displaying each individual line, not square, but line of a square.
    # This is because you have to print left to right and not up to down.

    def line_1(self):
        return "+-------+"

    def line_2(self):
        if self.is_path:
            return "|   X   |"
        elif self.is_base:
            return "|   b   |"
        else:
            return "|       |"
    
    def line_2_v_2(self):
        string = "|   "
        if self.is_path:
            string += "X"
        elif self.is_base:
            string += "b"
        else:
            string += " "
        string += "   |"
        return string

    def line_3_v2(self, num_enemies):
        if num_enemies > 0:
            if num_enemies >= 10:
                return "|  e " + str(num_enemies) + " |"
            else:
                return "|  e " + str(num_enemies) + "  |"
        elif self.tower != None:
            return "|   " + str(self.tower.get_tower_type()) + "   |"
        else:
            return "|       |"
    
    # Line 4 is displayign the health of certain things, like enemies or your base.
    # Your base is always displayed no matter what. Enemies however, only display their
    # health if they are the only one on that square.
    def line_4(self, base_health, max_base_health, enemy_health, max_enemy_health):
        if enemy_health > 0:
            if enemy_health < 10:
                if max_enemy_health < 10:
                    return "|  " + str(enemy_health) + "/" + str(max_enemy_health) + "  |"
                return "|  " + str(enemy_health) + "/" + str(max_enemy_health) + " |"
            else:
                if max_enemy_health < 10:
                    return "| " + str(enemy_health) + "/" + str(max_enemy_health) + "  |"
                return "| " + str(enemy_health) + "/" + str(max_enemy_health) + " |"
        elif self.is_base:
            if base_health < 10:
                if max_base_health < 10:
                    return "|  " + str(base_health) + "/" + str(max_base_health) + "  |"
                return "|  " + str(base_health) + "/" + str(max_base_health) + "|"
            elif base_health < 100:
                if max_base_health < 100:
                    return "| " + str(base_health) + "/" + str(max_base_health) + " |"
                return "| " + str(base_health) + "/" + str(max_base_health) + " |"
            else:
                if max_base_health > 99:
                    return "|" + str(base_health) + "/" + str(max_base_health) + "|"
                return "|" + str(base_health) + "/" + str(max_base_health) + " |"
        else:
            return "|       |"

    def line_5(self):
        return self.line_1()

# The board class creates a game_board of an array or arrays.
class Board:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.game_board = [] # game board is an array of arrays of
        for i in range(self.y):
            row = []
            for j in range(self.x):
                x, y = correct_coords(j, i, self.y)
                row.append(Square(x, y, None, False))
            self.game_board.append(row)
        self.towers = []
        self.enemies = [] # This is all of the alive enemies that are in the current wave that is happening.
        self.all_enemies = [] # This is all of the enemies that are alive and dead in the current wave.
        self.ordered_path = []
        self.base_health = 500
        self.max_base_health = self.base_health
        self.enemy_index = 0 # For displaying enemy info. DO NOT USE.
        self.wave_number = -1
        self.max_wave_number = -1

    def get_game_board(self):
        return self.game_board

    def get_enemies(self):
        return self.enemies
    
    def set_enemies(self, enemies):
        self.enemies = enemies

    def add_enemy(self, enemy):
        self.enemies.append(enemy)
        self.all_enemies.append(enemy)

    def get_towers(self):
        return self.towers

    def set_towers(self, towers):
        self.towers = towers

    def get_base_health(self):
        return self.base_health
    
    def set_base_health(self, base_health):
        self.base_health = base_health

    # This makes the base take damage.
    def base_take_damage(self, damage):
        self.base_health -= damage
        if self.base_health <= 0:
            self.base_health = 0
        return self.base_health

    def set_square(self, square):
        x = square.get_x()
        y = square.get_y()
        new_x, new_y = correct_coords(x, y, self.y)
        self.game_board[new_y][new_x] = square

    # This is to match up with Nicholas' and Richard's boards because I made my board different than your guys'.
    def convert(self):
        g_board = []
        for row in self.game_board:
            g_row = []
            for square in row:
                c = square.get_terrain()
                if c == "X":
                    if self.num_enemies_on_square(square.get_x(), square.get_y()) > 0:
                        c = "e"
                g_row.append(c)
            g_board.append(g_row)
        return g_board
    
    # This makes a list of coordinates which are the path coordinates.
    def add_path_in_order(self, square):
        self.set_square(square)
        self.ordered_path.append([square.get_x(), square.get_y()])

    def get_ordered_path(self):
        return self.ordered_path

    # This returns the coordinates of the base.
    # Btw, if you do not have a base on the board yet, you will get back [None, None] instead of [x, y].
    def board_get_base(self):
        for i in self.game_board:
            for square in i:
                if square.get_is_base():
                    return square.get_x(), square.get_y()
        return [None, None]


    def get_square(self, x, y):
        new_y = abs(y-(self.y-1))
        square = self.game_board[new_y][x]
        return square

    # This displays the game board.
    def display(self):
        self.enemy_index = 0
        buffer = "    "
        integer = self.y - 1
        for row in self.game_board:
            string_row_1 = "  "
            string_row_2 = "  "
            if integer < 10:
                string_row_3 = str(integer) + " "
                integer -= 1
            else:
                string_row_3 = str(integer) + ""
                integer -= 1
            string_row_4 = "  "
            string_row_5 = "  "
            for square in row:
                string_row_1 += square.line_1()
                string_row_2 += square.line_2_v_2()
                string_row_3 += square.line_3_v2(self.num_enemies_on_square(square.get_x(), square.get_y()))
                enemy_health, enemy_max_health = self.get_one_enemy_health(square.get_x(), square.get_y())
                string_row_4 += square.line_4(self.base_health, self.max_base_health, enemy_health, enemy_max_health)
                string_row_5 += square.line_5()
            
            if row == self.game_board[0]:
                string_row_1 += ""
                string_row_2 += ""
                if self.wave_number > 0:
                    string_row_3 += "           Current Wave:  " + str(self.wave_number) + "/" + str(self.max_wave_number)
                else:
                    string_row_3 += ""
                string_row_4 += ""
                string_row_5 += ""
            else:
                if row == self.game_board[1]:
                    string_row_1 += "               Enemy Info:"
                    string_row_2 += self.enemy_to_string()
                    string_row_3 += self.enemy_to_string()
                    string_row_4 += self.enemy_to_string()
                    string_row_5 += self.enemy_to_string()
                else:
                    string_row_1 += self.enemy_to_string()
                    string_row_2 += self.enemy_to_string()
                    string_row_3 += self.enemy_to_string()
                    string_row_4 += self.enemy_to_string()
                    string_row_5 += self.enemy_to_string()

            print(string_row_1)
            print(string_row_2)
            print(string_row_3)
            print(string_row_4)
            print(string_row_5)
        print("  " + buffer + '0' + buffer * 2 + '1' + buffer * 2 + '2' + buffer * 2 + '3' + buffer * 2 + '4' + buffer * 2 + '5' + buffer * 2 + '6' + buffer * 2 + '7' + buffer * 2 + '8' + buffer * 2 + '9')
        print()

    # This give you back the number of enemies on that x and y.
    def num_enemies_on_square(self, x, y):
        num_enemies = 0
        for enemy in self.enemies:
            if enemy.get_x() == x and enemy.get_y() == y:
                num_enemies += 1
        return num_enemies

    # This determines whether or not to display the enemies health. If there is more
    # than one enemy on that square, it does not display either of their healths.
    def get_one_enemy_health(self, x, y):
        current_health = 0
        max_health = 0
        for enemy in self.enemies:
            if enemy.get_x() == x and enemy.get_y() == y:
                if enemy.get_health() > 0:
                    if current_health > 0:
                        current_health = 0
                        max_health = 0
                        break
                    else:
                        current_health = enemy.get_health()
                        max_health = enemy.get_max_health()
        return current_health, max_health

    # This returns a string like "enemy1: 75/75(alive) coordinates: (4, 9)"
    def enemy_to_string(self):
        if self.enemy_index >= len(self.all_enemies):
            return ""
        enemy = self.all_enemies[self.enemy_index]
        self.enemy_index += 1
        string = "enemy" + str(self.enemy_index) + ": " + str(enemy.get_health()) + "/" + str(enemy.get_max_health()) + "("
        if enemy.get_health() <= 0:
            string += "dead)"
        else:
            string += "alive)"
        string += " coordinates: (" + str(enemy.get_x()) + ", " + str(enemy.get_y()) + ")"
        return string

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    # This removes an enemy from self.enemies
    def remove_enemy(self, dead_enemy):
        for enemy in self.enemies:
            if enemy == dead_enemy:
                self.enemies.remove(enemy)

def correct_coords(x, y, max_y):
    # Reversing the y index so that the bottom left corner is 0, 0.
    new_y = abs(y-(max_y-1))
    return [x, new_y]
