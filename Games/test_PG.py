import pygame

pygame.joystick.init()

joysticks = [ pygame.joystick.Joystick(x) for x in range( pygame.joystick.get_count() ) ]
print( "There are" , len( joysticks ) , "joysticks" )

for js in joysticks:
    js.init()
    print( "Joystick", js.get_id() , js.get_name() , "was initialized?:" , js.get_init() , "and has" , js.get_numaxes() , "axes and" ,
           js.get_numbuttons() , "buttons and" , js.get_numhats() , "hats" )

# ~~ SHUTDOWN ~~
pygame.joystick.quit()