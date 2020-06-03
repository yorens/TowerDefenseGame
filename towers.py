from math import sqrt
import random

class Towers:
    def __init__(self, tower_placement_x, tower_placement_y, tower_type, tower_strength):
        self.tower_placement_x = tower_placement_x
        self.tower_placement_y = tower_placement_y
        self.tower_type = tower_type
        self.tower_strength = tower_strength
        self.range = 2

    def get_tower_type(self):
        return self.tower_type[0]
        
    def get_tower_strength(self):
        return self.tower_strength

    #this function checks to see if a enemy exists
    def if_enemy_exists(self, board):
        for row in range(len(board[0])):
            for column in range(len(board)):
                if board[row][column][0] == 'e':
                    return True
        return False
                
    #this function gets the coordinates of all the path parts
    def path_coordinates(self, board):
        path_coords = []
        for row in range(10):
            for column in range(10):
                if board[row][column] == 'X' or board[row][column] == 'e':
                    path_coords.append([row, column])
        return path_coords
    
    #this sends a signal to the enemy to take damage.
    def shoot(self, board):
        if self.if_enemy_exists(board):
            return [True, self.tower_strength, self.find_enemy_closest_to_base(board)]
        return [False, 0, 0]

    def find_enemy_closest_to_base(self, board):
        if self.if_enemy_exists(board):
            path_coords = self.path_coordinates(board)
            for i in range(len(path_coords)):
                coord_check = path_coords[-i - 1]
                if board[coord_check[0]][coord_check[1]] == 'e':
                    return [coord_check[1], coord_check[0]]
        return False

            


