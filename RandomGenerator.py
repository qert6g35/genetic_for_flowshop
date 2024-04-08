import math
import random

class RandomGenerator:
    def __init__(self, seed):
        self.seed = seed
        random.seed(seed)

    def next_int(self):
        return random.randint(1, 30)