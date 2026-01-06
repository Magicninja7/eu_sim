import random

economy = 100
security = 100
people = 100
technology = 100

qs = [
    ['Criminality is on the rise!', ['Fund surveillance AI systems', [-10, +30, -40, +20]], ['Increase police presence', [-20, +10, -10, 0]]],
    ['The economy is struggling!', ['Invest in infrastructure', [+10, -10, +10, +10]], ['Cut taxes', [-20, +20, -10, -10]]],
    ['Technology development is stagnant!', ['Fund research grants', [-10, +10, +10, +20]], ['Encourage private sector innovation', [0, -10, +5, +30]]],
    ['Public health is overloaded!', ['Build more hospitals', [-30, +10, +20, +10]], ['Promote preventive care', [-10, 0, +10, 0]]],
    ['Energy prices spike!', ['Do nothing', [0, 0, -40, 0]], ['Subsidize households', [-30, +10, +20, 0]]],
    ['Big companies create a bad influence on people', ['Regulate them!!!!', [-20, +10, +20, -20]], ['Not our problem', [+20, -10, -20, +10]]],
    ['Big bad country wants to attack us!', ['Increase military spending', [-20, +30, -20, +10]], ['Appease them', [+10, -20, -20, +10]]],
    ['Memeber state breaking human rights!', ['Impose sanctions', [-10, 0, +20, 0]], ['Ignore it', [+10, 0, -20, 0]]],
    ['Foreign-funded media outlets spreading misinformation!', ['Ban them', [0, +20, -10, 0]], ['Informational campaign', [0, -20, +10, 0]]],
    ['Startups leave; too much regulations!', ["Didn't need them anyway", [-20, 0, +10, +10]], ['Ease regulation', [+10, -10, -10, +10]]],
    ['Agining population!', ['Raise retirement age', [+10, 0, -20, 0]], ['Do nothing', [-20, 0, +10, 0]]],
    ['Too much dependency on foreign sources of electricity!', ['Diversify sources', [-10, 10, 10, 0]], [['Do nothing'], [0, 0, 0, 0]]],
    ['Foreign surveillance drone crashes', ['Put sanctions on the country!', [-10, +10, +10, 0]], ['Invest in radar/AA systems', [-20, +20, +10, 0]]],
    ['Floods!', ['Limit environmental impact, invest in green energy', [-20, -10, +20, +10]], ['Do nothing', [+20, -10, -20, 0]]],
    ['New revolutionary technology!', ['Invest!!!!!!!', [+10, +10, +10, +10]], ['Leave to private sector', [+20, -10, -10, +20]]],
    ['Humanitarian crisis in the Middle East!', ['Provide aid to the region', [-10, 0, -10, 0]], ['Allow immigration', [+10, -30, +10, 0]]],
    ['Civilian plane shot down over foreign country!', ['Ask for apology', [0, -10, +5, 0]], ['Sanctions', [-20, +5, +10, 0]]],
    ['Foreign drone incursion!', ['Act of aggresion! (militarise)', [-30, +20, +30, 0]], ['Resolve issue diplomatically', [0, -10, +5, 0]]],
    ['Housing prices skyrocket!', ['Its the students, tourists & migrants!!!!', [-20, +5, +20, -20]], ['exponentially tax ownership of 3+ housing spaces', [+10, 0, -10, 0]]],
    ['Push through chat control?', ['Yes', [0, +20, -20, 0]], ['No', [0, -10, +10, 0]]],
    ['Cyberattack shuts down major bank!', ['Invest heavily in recovery', [-20, +20, +10, 0]], ['Let it stabilise naturally', [0, -0, -20, 0]]],
    ['Heatwave causes crops to die!!', ['Subsidize farmers', [-20, 0, +20, 0]], ['Do nothing', [+10, 0, -20, 0]]],
    ['Internet cables severed by foreign ship!', ['takeover said ship & input sanctions', [-20, +20, +10, 0]], ['Appease and resolve diplomatically', [+20, -10, 0, 0]]],
    ['Strategic ally commits war crimes!', ['Denounce & sanctions', [-10, -10, +20, 0]], ['Do nothing', [+10, +10, -20, 0]]],
    ['Protests block cities!', ['Crackdown', [+10, 0, -40, 0]], ['Try to appease', [-20, 0, +10, 0]]],
    ['Mass disinformation during election campaign!', ['Crack down on the posts', [-10, +10, -10, 0]], ['Do nothing', [0, -20, +10, 0]]],
    ['Foreign power imposes tarrifs!', ["Retaliate baxck with tarrifs!", [-30, +10, +10, 0]], ['Accept tarrifs', [-10, 0, -10, 0]]],
    ['Lake becomes contaminated!', ['Clean the water', [-20, 0, +10, 0]], ['Advise caution', [0, 0, -20, 0]]],
    ['New tech clashes with regulation', ['Ease regulation', [+20, -10, 0, 0]], ['Do nothing', [-10, 0, 0, 0]]],
    ['Spike in fraud targetting seniors', ['Awereness campaigns', [-10, 0, +10, 0]], ['Do nothing', [0, 0, -10, 0]]],
    ['Critical machine used in hospitals malfunctions!', ['Quit using immediately', [-20, +10, +10, +15]], ['Wait and monitor', [0, -10, -5, -10]]],
    ['Quantum research falls behind!', ['Invest heavily', [-25, 0, 0, +20]], ['Let private sector lead', [0, 0, 0, -15]]],
    ['Critical satellite malfunctions!', ['Repair immediately', [-20, +10, 0, +15]], ['Temporary, cheap, fixes', [0, -10, 0, -10]]],
    ['AI algorithms discriminate!', ['force to redesign algorithm', [-15, 0, +10, +10]], ['Ignore issue', [0, 0, -15, -5]]]
]

used = []
while economy>0 and security>0 and people>0 and technology>0:
    x = random.randint(0, 29)
    while x in used:
        x  = random.randint(0, 29)
    used.append(x)
    print('|  economy  | security |   people   | technology |')
    print(f'|    {economy}    |    {security}   |    {people}     |    {technology}     |\n')
    print(qs[x][0], '\n')
    print(f'1. {qs[x][1][0]}')
    print(f'2. {qs[x][2][0]}\n')
    ans = int(input('Option 1 or 2?\n'))
    print('\n')
    economy += int(qs[x][ans][1][0])
    security += int(qs[x][ans][1][1])
    people += int(qs[x][ans][1][2])
    technology += int(qs[x][ans][1][3])
    if economy > 100:
        economy = 100
    elif security > 100:
        security = 100
    elif people > 100:
        people = 100
    elif technology > 100:
        technology = 100
    if len(used) > 20:
        used = []

