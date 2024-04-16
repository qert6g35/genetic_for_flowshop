import math
import random

class RandomGenerator:
    """A random number generator class.

    Attributes:
        seed (int): The seed for random number generation.
    """

    def __init__(self, seed):
        """Initialize the RandomGenerator instance.

        Args:
            seed (int): The seed for random number generation.
        """
        self.seed = seed
        random.seed(seed)

    def next_int(self, low, high):
        """Generate a random integer between low and high (inclusive).

        Args:
            low (int): The lower bound of the range.
            high (int): The upper bound of the range.

        Returns:
            int: A random integer between low and high (inclusive).
        """
        return random.randint(low, high)