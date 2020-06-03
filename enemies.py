class Enemy:
    def __init__(self, health, damage, speed, location):
        self.max_health = health
        self.health = health
        self.damage = damage
        self.speed = speed
        self.location = location
        self.number = 0

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0

    def get_health(self):
        return self.health

    def get_max_health(self):
        return self.max_health

    def get_damage(self):
        return self.damage

    def get_x(self):
        return self.location[0]

    def get_y(self):
        return self.location[1]

    def move(self, path):
        self.number += 1
        if self.number >= len(path):
            return self.location
        self.location = path[self.number]
        return self.location
