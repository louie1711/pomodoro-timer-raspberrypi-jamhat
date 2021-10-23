# gpiozero contains the JamHat object (the little circuit board with the lights and buzzer on it)
from gpiozero import JamHat
from time import sleep
import math


######################################################### functions #########################################################
def play_end_timer_tune(jamhat): 
    jamhat.buzzer.play('C4')
    sleep(0.5)
    jamhat.off()

    jamhat.buzzer.play(70)
    sleep(0.5)
    jamhat.off()

    jamhat.buzzer.play(220.0)
    sleep(0.5)

######################################################### do the calculation to work out how many lights to turn on #########################################################
def calc_number_lights_to_switch_on(jamhat, loopcounter, selectedTimer ):
    # reset all lights
    jamhat.off()        
    totalNumLeds = 6
    gapForEachLight = float(selectedTimer) / float(totalNumLeds)

    numberOfLightsToLightNow = float(loopcounter) / float(gapForEachLight)    
    numberOfLightsToLightNow = math.ceil(numberOfLightsToLightNow)
    turnOnThisManyLights(jamhat, numberOfLightsToLightNow)

def turnOnThisManyLights(jamhat, numberOfLedsToLight):    
   
    print("numberOfLedsToLight = "+str(numberOfLedsToLight))
    lights = ["jamhat.lights_1.red.on()", "jamhat.lights_1.yellow.on()", "jamhat.lights_1.green.on()",
        "jamhat.lights_2.red.on()", "jamhat.lights_2.yellow.on()", "jamhat.lights_2.green.on()"]
    # loop array based on numberOfLedsToLight
    i = 0
    while i < numberOfLedsToLight:
        eval(lights[i])        # call eval on each element in the array , up to the count e.g. eval('aVar = aVar + 1')
        i += 1
    sleep(6)        # keeps the loop count timer the same (so all calculations should work on timting )

def turn_off_all_lights_and_turn_on_green_lights_to_indicate_ready(jamhat):    
   
    # reset it
    jamhat.off()
    # Turn the green lights on (indciates booted and program ready)
    jamhat.lights_1.green.on()
    jamhat.lights_2.green.on()    

######################################################### end of functions #########################################################
    
######################################################### start of main program #########################################################
# Initialise the JamHat object.
jamhat = JamHat()

turn_off_all_lights_and_turn_on_green_lights_to_indicate_ready(jamhat)

# 30 minutes timer  60 seconds * 30mins = 1800 seconds / 6 (each loop takes 6 seconds ) = 300
timerLength = 300  # 300 = 30 mins
# e.g. if you wanted a 5minute timer = 60 * 5 = 300 / 6 = 50
# timer = 50   # 5 minute timer

print ("funky timer bootingy !")

# Setup infinite loop in try / catch so user can CTRL+C terminate (if and only if keyboard attached)
try:
    while True:
        if(jamhat.button_1.is_pressed): # blue button            
            # each looper needs to go until 300 ( which is equal to 30 minutes )                                               
            loopcounter = 0

            selectedTimer = timerLength					

            while loopcounter < selectedTimer:
                calc_number_lights_to_switch_on(jamhat, loopcounter, selectedTimer)                
                loopcounter += 1    

            # loop ends after 30 minutes PLAY BUZZER
            play_end_timer_tune(jamhat)

        turn_off_all_lights_and_turn_on_green_lights_to_indicate_ready(jamhat)           
           
        sleep(0.1)

except KeyboardInterrupt:
    # If someone presses CTRL+C, close the JamHat, freeing of the Pins for use elsewhere.
    jamhat.close()

   