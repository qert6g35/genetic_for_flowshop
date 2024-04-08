from RandomGenerator import RandomGenerator 

seed = 123
generator = RandomGenerator(seed)

for _ in range(10):
    print(generator.next_int())
    