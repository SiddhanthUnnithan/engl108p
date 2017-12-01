from Card import Card, Suits

c = Card(Suits.CLUBS, '4')
cd = c.get_ascii_front()

for l in cd:
    print l