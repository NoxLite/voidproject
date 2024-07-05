import random

chance = []
for _ in range(60):
    chance.append('*')
for _ in range(40):
    chance.append('b')
for _ in range(5):
    chance.append('d')
for _ in range(5):
    chance.append('sd')


def random_generation():

    with open('./maps/RandomMap.txt', 'w') as f:
        map = []
        for i in range(15):
            line = []
            for j in range(15):
                if (i > 3 or j > 3) and (i < 12 or j < 12):
                    string = random.choice(chance)
                    line.append(string)
                else:
                    line.append('*')
            if i == 14:
                line[-1] = 'e'
            map.append(' '.join(line))
        result = '\n'.join(map)
        f.write(result)
