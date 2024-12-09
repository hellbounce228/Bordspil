from machine import Pin, PWM, ADC
import time
from time import sleep_ms
import random
from neopixel import NeoPixel

### BOARD VARIABLES
#joystick shit
xVal = ADC(Pin(5))
yVal = ADC(Pin(4))
xVal.atten(ADC.ATTN_11DB)
yVal.atten(ADC.ATTN_11DB)
xVal.width(ADC.WIDTH_12BIT)
yVal.width(ADC.WIDTH_12BIT)

#buttons/buttonlights
roll_button = Pin(42, Pin.IN, Pin.PULL_UP)  # button to press when you want to roll the wheel(neopixel)
finish_button = Pin(1, Pin.IN, Pin.PULL_UP)  # button to press when you finished your turn
roll_light = Pin(41, Pin.OUT)
finish_light = Pin(2, Pin.OUT)

#star lights
star_1_light = Pin(17, Pin.OUT)
star_2_light = Pin(40, Pin.OUT)
star_3_light = Pin(18, Pin.OUT)

# Reed switches
reed_switch_1 = Pin(15, Pin.IN, Pin.PULL_UP)  # Use internal pull-up resistor
reed_switch_2 = Pin(7, Pin.IN, Pin.PULL_UP)  # Use internal pull-up resistor
reed_switch_3 = Pin(6, Pin.IN, Pin.PULL_UP)  # Use internal pull-up resistor

#buzzer
buzzer = PWM(Pin(39), freq=10000, duty=0)

#neopixel
pin = Pin(8, Pin.OUT)
neo = NeoPixel(pin, 16)

### LISTS?
segments_score = {
    'a': Pin(35, Pin.OUT),
    'b': Pin(0, Pin.OUT),
    'c': Pin(45, Pin.OUT),
    'd': Pin(48, Pin.OUT),
    'e': Pin(47, Pin.OUT),
    'f': Pin(21, Pin.OUT),
    'g': Pin(36, Pin.OUT),
    'dp': Pin(19, Pin.OUT)
}

segments_player = {
    'a': Pin(3, Pin.OUT),
    'b': Pin(46, Pin.OUT),
    'c': Pin(9, Pin.OUT),
    'd': Pin(10, Pin.OUT),
    'e': Pin(11, Pin.OUT),
    'f': Pin(12, Pin.OUT),
    'g': Pin(13, Pin.OUT),
    'dp': Pin(14, Pin.OUT)
}

num_to_segments = {
    0: ['a', 'b', 'c', 'd', 'e', 'f'],
    1: ['b', 'c'],
    2: ['a', 'b', 'g', 'e', 'd'],
    3: ['a', 'b', 'g', 'c', 'd'],
    4: ['f', 'g', 'b', 'c'],
    5: ['a', 'f', 'g', 'c', 'd'],
    6: ['a', 'f', 'e', 'd', 'c', 'g'],
    7: ['a', 'b', 'c'],
    8: ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
    9: ['a', 'b', 'c', 'd', 'f', 'g'],
}


### FUNCTIONS

##CHECKING IF THE CHARACTER IS STANDING ON THE STARS 1,2,3

#first
def check_reed_switch_1():
    global current_star
    if current_star == 1:
        if reed_switch_1.value() == 0:  # Active state (switch closed)
            print("Magnet detected! 111")
            star_1_light.value(0)
            waiting_whatever = False
            players[turn_extra][1] += 1
            current_star = random.randint(1, 3)
        else:
            print("No magnet detected.")

#second
def check_reed_switch_2():
    global current_star
    if current_star == 2:
        if reed_switch_2.value() == 0:  # Active state (switch closed)
            star_2_light.value(0)
            players[turn_extra][1] += 1
            waiting_whatever = False
            print("Magnet detected! 222")

            current_star = random.randint(1, 3)
        else:
            print("No magnet detected.")

#third
def check_reed_switch_3():
    global current_star

    if current_star == 3:
        if reed_switch_3.value() == 0:  # Active state (switch closed)
            print("Magnet detected! 333")
            players[turn_extra][1] += 1
            waiting_whatever = False
            star_3_light.value(0)
            current_star = random.randint(1, 3)
        else:
            print("No magnet detected.")

        sleep_ms(500)  # Check every 100ms

##7-SEGMENT DISPLAYS

#display the score info
def display_number_score(num):
    # Turn off all segments
    for seg in segments_score.values():
        seg.value(1)
    # Turn on the required segments
    for seg in num_to_segments[num]:
        segments_score[seg].value(0)

#display the player info
def display_number_player(num):
    # Turn off all segments
    for seg in segments_player.values():
        seg.value(1)
    # Turn on the required segments
    for seg in num_to_segments[num]:
        segments_player[seg].value(0)

#waiting for the roll button
def wait_for_roll_button():
    while roll_button.value() == 1:  # Wait until button is pressed
        sleep_ms(100)  # Check every 10ms
    sleep_ms(50)  # Debounce delay
    while roll_button.value() == 0:  # Wait until button is released
        sleep_ms(1000)



while True:
    ### GETTING THE GAME READY
    players = []
    finish_light.value(0)
    turn_extra = -1
    turn = 0
    turn_count = 0
    player_amount = 0
    neo.fill([0, 0, 0])
    neo.write()
    star_3_light.value(0)
    star_2_light.value(0)
    star_1_light.value(0)
    waiting_for_the_player_choice = True
    player_amount_choice_allowed = False
    current_star = random.randint(1, 3)
    game_is_ongoing=True
    while game_is_ongoing:#GAME CYCLE/PROBS AFTER U FINISH THE STAR BULLSHIT
        print(players)
        waiting_for_the_finish_button_to_be_pressed = True
        waiting_for_the_roll_button_to_be_pressed = True
        while waiting_for_the_player_choice:
            # print('running')
            y_value = yVal.read()
            x_value = xVal.read()
            #print('x:', x_value, '  y:', y_value)
            time.sleep(0.2)
            if player_amount_choice_allowed == True and x_value < 100:
                print('choice made')
                waiting_for_the_player_choice = False
                for i in range(player_amount):
                    players.append([i + 1, 0])
                print(players)
            if x_value > 4050:
                print('up')
                player_amount_choice_allowed = True
                player_amount = 3
            elif y_value < 100:
                print('left')
                player_amount_choice_allowed = True
                player_amount = 4
            elif y_value > 4050:
                print('right')
                player_amount_choice_allowed = True
                player_amount = 2
            display_number_player(player_amount)
        turn += 1
        turn_extra += 1
        turn_count += 1

        if turn > player_amount:
            turn = 1
        if turn_extra == player_amount:
            turn_extra = 0
        display_number_player(turn)
        print("turn =", turn_count)

        if current_star == 1:
            star_1_light.value(1)
        elif current_star == 2:
            star_2_light.value(1)
        elif current_star == 3:
            star_3_light.value(1)
        print(current_star)
        for i in range(len(players)):
            
            if players[i][1]>=3:
                print(players[i][1])
                print('ending...')
                display_number_score(players[i][1])
                display_number_player(players[i][0])
                for i in range(3):    
                    buzzer.duty(500)
                    buzzer.freq(400)
                    sleep_ms(170)
                    buzzer.freq(250)
                    sleep_ms(70)
                    buzzer.freq(400)
                    sleep_ms(170)
                    buzzer.duty(0)
                game_is_ongoing=False
                
        for i in range(len(players)):
            if players[i][0] == turn:  # THE CODE HERE RUNS FOR THE PLAYER WHOS TURN IT IS
                neo.fill([0, 0, 0])
                neo.write()
                finish_light.value(0)
                print("player", i + 1, "is moving")
                print("player", i + 1, "has", players[i][1], "points")
                display_number_score(players[i][1])

                sleep_ms(1000)
                while waiting_for_the_roll_button_to_be_pressed:
                    roll_light.value(1)
                    if roll_button.value() == 0:
                        waiting_for_the_roll_button_to_be_pressed = False
                        roll_light.value(0)
                        wait_for_roll_button()
                        roll = random.randint(1, 4)
                        roll = random.randint(0, 15)
                        circles = random.randint(8, 10)
                        sleeptime = 10
                        for x in range(circles):
                            for spin in range(16):
                                buzzer.duty(500)
                                buzzer.freq(784)
                                sleep_ms(10)
                                buzzer.duty(0)
                                neo.fill([0, 0, 0])
                                neo[spin] = [0, 5, 0]
                                sleep_ms(sleeptime)
                                neo.write()
                                spins = circles * 16
                                if x > circles - 5:
                                    sleeptime += 1
                                if x > circles - 3:
                                    sleeptime += 2
                        for y in range(roll):
                            buzzer.duty(500)
                            buzzer.freq(784)
                            sleep_ms(10)
                            buzzer.duty(0)
                            neo.fill([0, 0, 0])
                            neo[y] = [0, 5, 0]
                            sleeptime += 5
                            sleep_ms(sleeptime)
                            neo.write()

                        if roll == 1 or roll == 2 or roll == 3 or roll == 4:
                            neo.fill([0, 0, 0])
                            neo[1] = [0, 5, 0]
                            neo[2] = [0, 5, 0]
                            neo[3] = [0, 5, 0]
                            neo[4] = [0, 5, 0]
                            
                            neo.write()
                            
                            buzzer.duty(500)
                            buzzer.freq(523)
                            sleep_ms(100)
                            buzzer.freq(659)
                            sleep_ms(100)
                            buzzer.duty(784)
                            sleep_ms(300)
                            buzzer.duty(0)
                        elif roll == 5 or roll == 6 or roll == 7 or roll == 8:
                            neo.fill([0, 0, 0])
                            neo[5] = [0, 5, 0]
                            neo[6] = [0, 5, 0]
                            neo[7] = [0, 5, 0]
                            neo[8] = [0, 5, 0]
                            
                            neo.write()
                            
                            buzzer.duty(500)
                            buzzer.freq(523)
                            sleep_ms(100)
                            buzzer.freq(659)
                            sleep_ms(100)
                            buzzer.duty(784)
                            sleep_ms(300)
                            buzzer.duty(0)
                        elif roll == 9 or roll == 10 or roll == 11 or roll == 12:
                            neo.fill([0, 0, 0])
                            neo[9] = [0, 5, 0]
                            neo[10] = [0, 5, 0]
                            neo[11] = [0, 5, 0]
                            neo[12] = [0, 5, 0]
                            
                            neo.write()
                            
                            buzzer.duty(500)
                            buzzer.freq(523)
                            sleep_ms(100)
                            buzzer.freq(659)
                            sleep_ms(100)
                            buzzer.duty(784)
                            sleep_ms(300)
                            buzzer.duty(0)
                        elif roll == 13 or roll == 14 or roll == 15 or roll == 0:
                            neo.fill([0, 0, 0])
                            neo[13] = [0, 5, 0]
                            neo[14] = [0, 5, 0]
                            neo[15] = [0, 5, 0]
                            neo[0] = [0, 5, 0]
                            
                            neo.write()
                            
                            buzzer.duty(500)
                            buzzer.freq(523)
                            sleep_ms(100)
                            buzzer.freq(659)
                            sleep_ms(100)
                            buzzer.duty(784)
                            sleep_ms(300)
                            buzzer.duty(0)
                            
                sleep_ms(1000)
                waiting_whatever = True
                while waiting_for_the_finish_button_to_be_pressed:
                    
                    if current_star == 1:
                        if reed_switch_1.value() == 0:  # Active state (switch closed)
                            star_1_light.value(0)
                            sleep_ms(250)
                            star_1_light.value(1)
                            sleep_ms(250)
                            
                    if current_star == 2:
                        if reed_switch_2.value() == 0:  # Active state (switch closed)
                            star_2_light.value(0)
                            sleep_ms(250)
                            star_2_light.value(1)
                            sleep_ms(250)
                            
                    if current_star == 3:
                        if reed_switch_3.value() == 0:  # Active state (switch closed)
                            star_3_light.value(0)
                            sleep_ms(250)
                            star_3_light.value(1)
                            sleep_ms(250)
                
                    finish_light.value(1)
                    
                    if finish_button.value() == 0:
                        waiting_for_the_finish_button_to_be_pressed = False
                        
                        check_reed_switch_1()
                        check_reed_switch_2()
                        check_reed_switch_3()
                        
                        finish_light.value(0)
                        
                        buzzer.duty(500)
                        buzzer.freq(261)
                        sleep_ms(170)
                        buzzer.freq(523)
                        sleep_ms(70)
                        buzzer.freq(261)
                        sleep_ms(170)
                        buzzer.duty(0)
                        continue
