import random
solution = [g for g in range(0,16)]
solution = [g for g in range(0,16)]

print(solution)
print(solution)


newchild = solution[random.randint(1, int(len(solution) - 1)):]
newchild += [gene for gene in solution if gene not in newchild]

print(newchild)


