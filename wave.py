# Wave class simply has the wave number, say the 3rd wave or 3, and 
# it has a list of enemies in that specific wave.
class Wave:
    def __init__(self, wave_number):
        self.wave_number = wave_number
        self.wave_enemies = []

    # adds enemies to waves.
    def add_enemy(self, enemy):
        self.wave_enemies.append(enemy)