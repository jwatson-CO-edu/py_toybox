from vpython import *
from math import sqrt, cos, sin, pi

sqrt2 = sqrt(2)

# xFactors = [ +sqrt2 , -sqrt2 ]

shipGreen  = vec( 0.0 , 1.0 , 0.0 ) #vector(106/255, 196/255, 124/255)
shipBlue   = vec( 69/255, 118/255, 255/255 ) #vector(106/255, 124/255 , 196/255)
shipOrange = vec( 1.0 , 0.0 , 0.0 ) #vector(255/255, 148/255, 54/255)
BGcolor    = vec( 0.0 , 0.0 , 0.0 ) #vec(48/255, 8/255, 8/255)
trailColor = vec( 1.0 , 1.0 , 0.0 ) #vector( 255/255, 244/255, 25/255 )

scene.background = BGcolor
scene.width      = 800
scene.height     = 800

shipGeo = compound( [

    cone( axis = vector( 0 , 0 , 8 ) , 
          radius = 3.0 , 
          color = shipGreen ),
          
    cone( axis = vector( 0 , 0 , -4 ) , 
          radius = 3.0 , 
          color = shipGreen ),

    triangle(
        v0=vertex( pos=vec(0,0,0) , color = shipOrange ),
        v1=vertex( pos=vec(0,0,8) , color = shipOrange ),
        v2=vertex( pos=vec(0,6,-4) , color = shipOrange ) , 
        color = vector(106/255, 196/255, 124/255) 
    ),

    triangle(
        v0=vertex( pos=vec(0,0,0) , color = shipBlue ),
        v1=vertex( pos=vec(0,0,8) , color = shipBlue ),
        v2=vertex( pos=vec(-6,-6,-4) , color = shipBlue ) , 
        color = vector(106/255, 196/255, 124/255) 
    ),

    triangle(
        v0=vertex( pos=vec(0,0,0) , color = shipBlue ),
        v1=vertex( pos=vec(0,0,8) , color = shipBlue ),
        v2=vertex( pos=vec(+6,-6,-4) , color = shipBlue ) , 
        color = vector(106/255, 196/255, 124/255) 
    ),
],make_trail=True, retain=20, trail_color=trailColor)

orbitRad = 60.0
theta    =  0.0
FPS      = 50
angSpeed = 0.0625/4.0

shipGeo.rotate( angle = -pi/2.0 , axis=vector(1.0,0.0,0.0) )

print( vars( shipGeo ) )

while 1:
    rate( FPS )
    shipGeo.rotate( angle = angSpeed , axis=vector(0.0,0.0,1.0) )
    theta += angSpeed
    Xs = orbitRad * cos( theta )
    Ys = orbitRad * sin( theta )
    shipGeo.pos = vec( Xs , Ys , 0.0 )

#for xFact in xFactors:
#    triangle(
#        v0=vertex( pos=vec(0,0,0) , color = shipBlue ),
#        v1=vertex( pos=vec(8,0,0) , color = shipBlue ),
#        v2=vertex( pos=vec(-4,6*xFact,xFact) , color = shipBlue ) , 
#        color = vector(106/255, 196/255, 124/255) 
#    )
          
