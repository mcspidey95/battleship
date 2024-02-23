from engine import Game
import matplotlib.pyplot as pt

games = 100
shots1, shots2 = [],[]
values1, values2 = [],[]
avg1, avg2 = 0,0

for i in range(games):
    game = Game(human1=False,human2=False)
    while not game.over:
        game.basic_ai()
    shots1.append(game.shots//2)
avg1=sum(shots1)/len(shots1)

for i in range(games):
    game = Game(human1=False,human2=False)
    while not game.over:
        game.human_ai()
    shots2.append(game.shots//2)
avg2=sum(shots2)/len(shots2)


for i in range(17,100):
    values1.append(shots1.count(i))

for i in range(17,100):
    values2.append(shots2.count(i))


pt.style.use('ggplot')
pt.plot(range(17,100), values1, label='basic_ai')
pt.plot(range(17,100), values2, label='human_ai')
pt.legend()
pt.show()

pt.bar('basic_ai',avg1)
pt.bar('human_ai',avg2)
pt.show()

print(shots2)
print('basic_ai average moves: ',avg1)
print('human_ai average moves: ',avg2)