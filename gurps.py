import random

def r3d():
    return(random.randint(1,6)+random.randint(1,6)+random.randint(1,6))
def skill_check(skill,skill_name):
    x=r3d()
    print(skill_name+': '+str(x)+' против '+str(skill))
    a=[x,x-int(skill)]
    return(a)
    
class ship:
    def __init__(self,SM,DR,hp,hnd,acceleration,deltaV_max,deltaV,gun_damage,sAcc,dodge,leadership,spacer,shiphandling,navigation_space,tactics,piloting,gunner_beams):
        self.SM=SM
        self.DR=DR
        self.hp=hp
        self.hnd=hnd
        self.acceleration=acceleration
        self.deltaV_max=deltaV_max
        self.deltaV=deltaV
        self.gun_damage=gun_damage
        self.sAcc=sAcc
        self.dodge=dodge
        self.leadership=leadership
        self.spacer=spacer
        self.shiphandling=shiphandling
        self.tactics=tactics
        self.navigation_space=navigation_space
        self.piloting=piloting
        self.gunner_beams=gunner_beams
        self.dodge_bonus=0
    def damage(self,gun_damage):
        damage=0
        for i in range(gun_damage):
            damage+=random.randint(1,6)
        return(damage)
    def onHit(self,damage,modifier):
        check = skill_check(self.dodge+modifier+self.dodge_bonus,'Уклонение')
        if check[1]>0:
            if damage>self.DR:
                self.hp=self.hp-(damage-self.DR)
                print('Попадание на',damage-self.DR,'урона')
            else:
                print('Не пробил!')
        else:
            print('Цель уклонилась!')
        
def one_space_turn(player,counter,ship,enemy,distance):
    print(counter,'ход',player)
    print('Фаза 1: Командование')
    print('Доступные действия:')
    print('1) Лидерство')
    print('2) Кораблевождение')
    print('3) Космическая тактика')
    print('Помощь')
    pilot_shiphndl=0
    e_dodge=0
    ship.dodge_bonus=0
    prompt=''
    loop=1
    advantaged=0
    temp_distance=0
    spacer=ship.spacer
    while loop==1:
        loop=0
        prompt=input()
        if prompt == '1':
            check=skill_check(ship.leadership,'Лидерство')
            if (check[1]<=-5) or (check[0]<=4):
                spacer+=1
        elif prompt == '2':
            if ship.shiphandling<spacer:
                check=skill_check(ship.shiphandling,'Кораблевождение')
                if (check[1]<=-5) or (check[0]<=4):
                    pilot_shiphndl=check[1]
            else:
                check=skill_check(spacer,'Космонавт')
                if (check[1]<=-5) or (check[0]<=4):
                    pilot_shiphndl=check[1]
        elif prompt == '3':
            print('1) Атакующая тактика')
            print('2) Защитная тактика')
            loop1=1
            while loop1==1:
                loop1=0
                prompt=input()
                if prompt == '1':
                    check=skill_check(min(ship.navigation_space,ship.tactics),'Навигация (Космос)/Тактика (меньшее)')
                    if check[1]<=0:
                        e_dodge=-1
                    elif check[1]<=-10:
                        e_dodge-=2
                elif prompt == '2':
                    check=skill_check(min(ship.navigation_space,ship.tactics),'Навигация (Космос)/Тактика (меньшее)')
                    if check[1]<=0:
                        ship.dodge_bonus=1
                    elif check[1]<=-10:
                        ship.dodge_bonus=2
                else:
                    print('Недействительный параметр')
                    loop1=1
        elif prompt == 'Помощь':
            print('GURPS Spaceships стр. 50-51')
            print('Лидерство: успешный бросок помимо стандартных эффектов увеличивает значение навыка Космонавт команды на 1')
            print('Кораблевождение: успешный бросок минимального из навыков Кораблевождение капитана и навыка Космонавт экипажа считается успешным маневром пилотирования')
            print('Космическая тактика: успешный бросок минимального из навыков Навигация (Космос) и Тактика совершается для выполнения следующих действий. Атакующая тактика уменьшает параметр уклонения противника на 1, защитная тактика увеличивает уклонение собственного корабля на 1. Критический успех удваивает эффект.')
            loop=1
        else:
            print('Недействительный параметр')
            loop=1
    print('Фаза 4: Пилотирование')
    print('Доступные действия:')
    print('1) Сближение')
    print('2) Контролируемый дрейф')
    print('3) Уклонение')
    #print('4) Держать курс')
    print('5) Отступление')
    #print('6) Неконтролируемый дрейф')
    print('Помощь')
    loop=1
    while loop==1:
        loop=0
        prompt=input()
        if prompt == '1':
            if ship.deltaV>min_burn: #топлива хватает для бонуса манневра
                ship.deltaV-=min_burn
                if pilot_shiphndl>0:
                    check=skill_check(ship.piloting+ship.hnd, 'Пилотирование')
                if ((check[1]<=-10) or (pilot_shiphndl<=-10)) and (distance==0):
                    print('Критический успех!')
                    print('1) Получить расстояние Атакующий вектор + статус Преимущество')
                    print('2) Получить статус расстояния Сближения')
                    print('3) Получить расстояние Курс на столкновение')
                    loop1=1
                    while loop1==1:
                        loop1=0
                        prompt = input()
                        if prompt=='1':
                            advantaged=1
                            temp_distance=1
                        elif prompt=='2':
                            distance=1
                        elif prompt=='3':
                            temp_distance=2
                        else:
                            print('Недействительный параметр')
                            loop1=1
                elif ((check[1]<=-10) or (pilot_shiphndl<=-10)) and (distance==1):
                    print('Критический успех!')
                    print('1) Получить расстояние Курс на столкновение + статус Преимущество')
                    print('2) Получить статус расстояния Рандеву')
                    loop1=1
                    while loop1==1:
                        loop1=0
                        prompt = input()
                        if prompt=='1':
                            advantaged=1
                            temp_distance=2 
                        elif prompt=='2':
                            distance=4
                        else:
                            print('Недействительный параметр')
                            loop1=1
                elif ((check[1]<=0) or (pilot_shiphndl<=0)) and (distance==0):
                    print('Успех!')
                    print('1) Получить расстояние Атакующий вектор')
                    print('2) Получить статус Преимущество')
                    loop1=1
                    while loop1==1:
                        loop1=0
                        prompt = input()
                        if prompt=='1':
                            temp_distance=1
                        elif prompt=='2':
                            advantaged=1
                        else:
                            print('Недействительный параметр')
                            loop1=1
                elif ((check[1]<=0) or (pilot_shiphndl<=0)) and (distance==1):
                    print('Успех!')
                    print('1) Получить расстояние Курс на столкновение')
                    print('2) Получить статус Преимущество')
                    loop1=1
                    while loop1==1:
                        loop1=0
                        prompt = input()
                        if prompt=='1':
                            temp_distance=2 
                        elif prompt=='2':
                            advantaged=1
                        else:
                            print('Недействительный параметр')
                            loop1=1
                #facing=0
                escape=0
            else:
                print('Топлива недостаточно для ускорения!')
                loop=1
                
        elif prompt=='2':
            escape=0
            """print('facing (1-front, 2-center 3-rear')"""
                
        elif prompt == '3':
            if ship.deltaV>min_burn: #топлива хватает для бонуса манневра
                ship.deltaV-=min_burn
                ship.dodge+=1
                distance=0
                escape=1
                #facing=[1,2]
            else:
                print('Топлива недостаточно для ускорения!')
                loop=1
        elif prompt == '5':
            if (ship.deltaV>min_burn) and (escape>=1): #топлива хватает для бонуса манневра
                if escape>=2:
                    print('Возможность для выхода из боя. Необходимо вмешательство гейм-мастера')
                escape+=1
                ship.deltaV-=min_burn
            else:
                print('Не достаточно топлива и/или не выполнен манневр Уклонения')
                loop=1
        elif prompt == 'Помощь':
            print('GURPS Spaceships стр. 55-57')
            print('Сближение - сократить дистанцию с противником. При успехе временно сокращает дистанцию, что увеличивает шанс попадания либо даёт бонус к атаке +2. При критическом успехе дает возможность взять оба предыдущих варианта, либо перманентно сократить расстояние с противником (пока он не совершит манневр, требующий ускорение), либо временно сократить дистанцию на два пункта. Требуется ускорение.')
            print('Контролируемый дрейф - манневр, не требующий ускорения. Сохраняет перманентные позиции.')
            print('Уклонение - автоматически сбрасывает перманентное расстояние до начального, увеличивает уклонение на 1. Требует ускорения.')
            print('Отступление - попытка выйти из боя. Для активации требует ускорения и манневра уклонения в прошлом ходу. Выход из боя происходит в следующем ходу, требуется вмешательство гейм-мастера.')
        else:
            print('Недействительный параметр')
            loop=1
    print('Фаза 6: Стрельба')
    print('Доступные действия:')
    print('1) Прицелиться и выстрелить')
    #print('2) Ожидание (Прицелиться и выстрелить)')
    #print('3) Ожидание (Точечная защита)')
    space_range_close = ['Short','Close','Point-blank','Point-blank','Zero']
    space_range_standart = ['Long','Short','Close','Point-blank','Zero']
    space_range_distant = ['Extreme','Long','Short','Point-blank','Zero']
    space_range_table = {'Zero':20,'Point-blank':0,'Close':-4,'Short':-8,'Long':-12,'Extreme':-16}
    if combat_scale == 'close':
        space_range = space_range_table[space_range_close[max(distance,temp_distance)]]
    elif combat_scale == 'standart':
        space_range = space_range_table[space_range_standart[max(distance,temp_distance)]]
    else:
        space_range = space_range_table[space_range_distant[max(distance,temp_distance)]]
    loop=1
    while loop==1:
        loop=0
        prompt=input()
        if prompt == '1':
            check=skill_check(ship.gunner_beams+enemy.SM+ship.sAcc+space_range+2*advantaged,'Тяжёлое оружие (Лучевое)')
            if check[1]<=0:
                print('Успех!')
                enemy.onHit(ship.damage(ship.gun_damage),e_dodge)
            else:
                print('Промах!')
        else:
            print('Недействительный параметр')
            loop=1
    print('Текущая дистанция:',distance)
    
prompt=''
print('Симулятор космических боев по правилам GURPS Spaceships')
print('Выберите шаблон корабля:')
print('1) Космический крейсер класса Победа')
print('2) Фрегат класса Деймос')
print('3) Дальнобойщик класса Такаяма')
loop=1
while loop==1:
    loop=0
    prompt=input()
    if prompt == '1':
        print('Текущие запасы топлива (не более 40)')
        loop1=1
        while loop1==1:
            loop1=0
            prompt=input()
            if (float(prompt)<=40) and (float(prompt)>=0):
                deltaV=float(prompt)
            else:
                print('Повторите ввод')
                loop1=1
        print('Навыки экипажа (10 для новичков, 11 для средних, 12 для опытных, 13 для ветеранов, 14 для элиты)')
        print('Лидерство')
        leadership=int(input())
        print('Космонавт')
        spacer=int(input())
        print('Кораблевождение')
        shiphandling=int(input())
        print('Навигация (Космос)')
        navigation_space=int(input())
        print('Тактика')
        tactics=int(input())
        print('Пилотирование')
        piloting=int(input())
        print('Тяжелое оружие (Лучевое)')
        gunner_beams=int(input())
        dodge=int(piloting/2-2)
        #SM,DR,hp,hnd,acceleration,deltaV_max,deltaV,gun_damage,sAcc,dodge,leadership,spacer,shiphandling,navigation_space,tactics,piloting,gunner_beams):
        player1=ship(10,100,150,-2,0.1,40,deltaV,30,-3,dodge,leadership,spacer,shiphandling,navigation_space,tactics,piloting,gunner_beams)
        p1_max_range='long'
    elif prompt == '2':
        print('Текущие запасы топлива (не более 40)')
        loop1=1
        while loop1==1:
            loop1=0
            prompt=input()
            if (float(prompt)<=40) and (float(prompt)>=0):
                deltaV=float(prompt)
            else:
                print('Повторите ввод')
                loop1=1
        print('Навыки экипажа (10 для новичков, 11 для средних, 12 для опытных, 13 для ветеранов, 14 для элиты)')
        print('Лидерство')
        leadership=int(input())
        print('Космонавт')
        spacer=int(input())
        print('Кораблевождение')
        shiphandling=int(input())
        print('Навигация (Космос)')
        navigation_space=int(input())
        print('Тактика')
        tactics=int(input())
        print('Пилотирование')
        piloting=int(input())
        print('Тяжелое оружие (Лучевое)')
        gunner_beams=int(input())
        dodge=int(piloting/2-2)
        player1=ship(8,32,70,-2,0.15,40,deltaV,20,0,dodge,leadership,spacer,shiphandling,navigation_space,tactics,piloting,gunner_beams)
        p1_max_range='long'
    elif prompt == '3':
        print('Текущие запасы топлива (не более 20)')
        loop1=1
        while loop1==1:
            loop1=0
            prompt=input()
            if (float(prompt)<=40) and (float(prompt)>=0):
                deltaV=float(prompt)
            else:
                print('Повторите ввод')
                loop1=1
        print('Навыки экипажа (10 для новичков, 11 для средних, 12 для опытных, 13 для ветеранов, 14 для элиты)')
        print('Лидерство')
        leadership=int(input())
        print('Космонавт')
        spacer=int(input())
        print('Кораблевождение')
        shiphandling=int(input())
        print('Навигация (Космос)')
        navigation_space=int(input())
        print('Тактика')
        tactics=int(input())
        print('Пилотирование')
        piloting=int(input())
        print('Тяжелое оружие (Лучевое)')
        gunner_beams=int(input())
        dodge=int(piloting/2-1)
        player1=ship(9,4,100,-1,1.5,20,deltaV,4,0,dodge,leadership,spacer,shiphandling,navigation_space,tactics,piloting,gunner_beams)
        p1_max_range='long'
    else:
        print('Повторите ввод')
        loop=1
print('Выберите корабль оппонента (1-3)')
loop=1
while loop==1:
    loop=0
    prompt=input()
    if prompt == '1':
        print('Текущие запасы топлива (не более 40)')
        loop1=1
        while loop1==1:
            loop1=0
            prompt=input()
            if (float(prompt)<=40) and (float(prompt)>=0):
                deltaV=float(prompt)
            else:
                print('Повторите ввод')
                loop1=1
        print('Навыки экипажа (10 для новичков, 11 для средних, 12 для опытных, 13 для ветеранов, 14 для элиты)')
        print('Лидерство')
        leadership=int(input())
        print('Космонавт')
        spacer=int(input())
        print('Кораблевождение')
        shiphandling=int(input())
        print('Навигация (Космос)')
        navigation_space=int(input())
        print('Тактика')
        tactics=int(input())
        print('Пилотирование')
        piloting=int(input())
        print('Тяжелое оружие (Лучевое)')
        gunner_beams=int(input())
        dodge=int(piloting/2-2)
        player2=ship(10,100,150,-2,0.1,40,deltaV,30,-3,dodge,leadership,spacer,shiphandling,navigation_space,tactics,piloting,gunner_beams)
        p2_max_range='long'
    elif prompt == '2':
        print('Текущие запасы топлива (не более 40)')
        loop1=1
        while loop1==1:
            loop1=0
            prompt=input()
            if (float(prompt)<=40) and (float(prompt)>=0):
                deltaV=float(prompt)
            else:
                print('Повторите ввод')
                loop1=1
        print('Навыки экипажа (10 для новичков, 11 для средних, 12 для опытных, 13 для ветеранов, 14 для элиты)')
        print('Лидерство')
        leadership=int(input())
        print('Космонавт')
        spacer=int(input())
        print('Кораблевождение')
        shiphandling=int(input())
        print('Навигация (Космос)')
        navigation_space=int(input())
        print('Тактика')
        tactics=int(input())
        print('Пилотирование')
        piloting=int(input())
        print('Тяжелое оружие (Лучевое)')
        gunner_beams=int(input())
        dodge=int(piloting/2-1)
        player2=ship(8,32,70,-2,0.15,40,deltaV,20,0,dodge,leadership,spacer,shiphandling,navigation_space,tactics,piloting,gunner_beams)
        p2_max_range='long'
    elif prompt == '3':
        print('Текущие запасы топлива (не более 20)')
        loop1=1
        while loop1==1:
            loop1=0
            prompt=input()
            if (float(prompt)<=40) and (float(prompt)>=0):
                deltaV=float(prompt)
            else:
                print('Повторите ввод')
                loop1=1
        print('Навыки экипажа (10 для новичков, 11 для средних, 12 для опытных, 13 для ветеранов, 14 для элиты)')
        print('Лидерство')
        leadership=int(input())
        print('Космонавт')
        spacer=int(input())
        print('Кораблевождение')
        shiphandling=int(input())
        print('Навигация (Космос)')
        navigation_space=int(input())
        print('Тактика')
        tactics=int(input())
        print('Пилотирование')
        piloting=int(input())
        print('Тяжелое оружие (Лучевое)')
        gunner_beams=int(input())
        dodge=int(piloting/2-1)
        player2=ship(9,4,100,-1,1.5,20,deltaV,4,0,dodge,leadership,spacer,shiphandling,navigation_space,tactics,piloting,gunner_beams)
        p2_max_range='long'
    else:
        print('Повторите ввод')
        loop=1
#phase 0
#scale
if (((player1.deltaV < 5) or (player2.deltaV < 5)) or ((p1_max_range == 'short') or (p2_max_range == 'short')) and player1.acceleration < 50 and player2.acceleration < 50):
    combat_scale = 'close'
    print('Оптимальные расстояния от 20 до 2000 миль')
elif ((p1_max_range == 'long') or (p1_max_range == 'long') or (player1.acceleration > 0.5 and player1.acceleration < 500) or (player2.acceleration > 0.5 and player2.acceleration < 500)):
    combat_scale = 'standart'
    print('Оптимальные расстояния от 200 до 20000 миль')
else:
    combat_scale = 'distant'
    print('Оптимальные расстояния от 2000 до 200000 миль')
#turn length
acceleration_chart = [0,0.05,0.5,10,50,500]
close_scale = ['10 минут','3 минуты','1 минута','20 секунд','20 секунд*','20 секунд*']
standart_scale = ['10 минут**','10 минут','3 минуты','1 минута','20 секунд','20 секунд*']
distant_scale = ['10 минут**','10 минут**','10 минут','3 минуты','1 минута','20 секунд']
loop=1
while loop==1:
    print('Выбрать длительность хода вручную? да/нет')
    loop=0
    for i in range(6):
        if max(player1.acceleration,player2.acceleration)>acceleration_chart[i]:
            order=i
    prompt=input()
    if prompt=='да':
        loop1 = 1
        print(close_scale[order],standart_scale[order],distant_scale[order])
        print('Длительность хода: [выберете подходящую длительность и напишите номер соответсвтующей позиции (1-3)]')
        print('* - манневренность кораблей слишком маленькая для данного масштаба – тактика будет сильно зависеть от контроля урона и оружейного огня')
        print('** - скорость кораблей слишком большая для оптимального расстояния')
        while (loop1==1):
            x=input()
            if (int(x)>=1 or int(x)<=3):
                if x == '1':
                    turn_length = [close_scale,order]
                elif x=='2':
                    turn_length = [standart_scale,order]
                elif x=='3':
                    turn_length = [distant_scale,order]
                loop1=0
            else:
                print('Недействительный параметр')
    elif prompt=='нет':
        if combat_scale == 'close':
            print('Длительность хода:',close_scale[order])
            turn_length = [close_scale,order]
        elif combat_scale == 'standart':
            print('Длительность хода:',standart_scale[order])
            turn_length = [standart_scale,order]
        else:
            print('Длительность хода:',distant_scale[order])
            turn_length = [distant_scale,order]
    else:
        print('Некорректный формат, повторите ввод еще раз')
        loop=1
acc_bonus_10min={'close':0.03,'standart':0.3,'distant':3}
acc_bonus_3min={'close':0.01,'standart':1,'distant':10}
acc_bonus_1min={'close':0.3,'standart':3,'distant':30}
acc_bonus_20sec={'close':1,'standart':10,'distant':100}
if turn_length[0][turn_length[1]].startswith('10'):
    min_burn=acc_bonus_10min[combat_scale]
elif turn_length[0][turn_length[1]].startswith('3 '):
    min_burn=acc_bonus_3min[combat_scale]
elif turn_length[0][turn_length[1]].startswith('1 '):
    min_burn=acc_bonus_1min[combat_scale]
else:
    min_burn=acc_bonus_20sec[combat_scale]
print('Кто ходит первым?')
print('1) Игрок')
print('2) Противник')
prompt=input()
if prompt =='1':
    turn_order_name=['игрока','противника']
    turn_order=[player1,player2]
else:
    turn_order_name=['противника','игрока']
    turn_order=[player2,player1]
counter=1
distance=0
while ((player1.hp>0) and (player2.hp>0)):
    one_space_turn(turn_order_name[0], counter, turn_order[0], turn_order[1],distance)
    print('Текущее здоровье игрока: '+str(player1.hp))
    print('Текущее здоровье противника: '+str(player2.hp))
    print('Текущие запасы топлива игрока:',player1.deltaV)
    print('Текущие запасы топлива противника:',player2.deltaV)
    counter+=1
    one_space_turn(turn_order_name[1], counter, turn_order[1], turn_order[0],distance)
    print('Текущее здоровье игрока: '+str(player1.hp))
    print('Текущее здоровье противника: '+str(player2.hp))
    print('Текущие запасы топлива игрока:',player1.deltaV)
    print('Текущие запасы топлива противника:',player2.deltaV)
    counter+=1
if (player1.hp<=0):
    print('Корабль игрока уничтожен!')
else:
    print('Корабль противника уничтожен! Победа!')