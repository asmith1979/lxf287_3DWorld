# Script: Wolf3DExamp.py
# Adapted by Andrew Smith
# Date: November 2021
# Description: LXF286 Python coding tutorial (Part 1)
#              Looks at loading 3D world, player movement / mechanics

import pygame
from pygame.locals import *
import math
import worldManager
import time

####  WALL TEXTURES   #####
# 8 - Colourstone
# 7 - Wood
# 6 - Mossy
# 5 - Bluestone
# 4 - Greystone
# 3 - Redbrick
# 2 - Purplestone
# 1 - Eagle

worldMap =[
 [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
 [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
 [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
 [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
 [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
 [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
 [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
 [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
 [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
 [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
 [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
 [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
 [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
 [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
 [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
 [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
 [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
 [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
 [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
 [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
 [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
 [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
 [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4]
];



sprite_positions=[
  (20.5, 11.5, 2), #green light in front of playerstart
  #green lights in every room
  (18.5,4.5, 2),
  (10.0,4.5, 2),
  (10.0,12.5,2),
  (3.5, 6.5, 2),
  (3.5, 20.5,2),
  (3.5, 14.5,2),
  (14.5,20.5,2),
  
  #row of pillars in front of wall: fisheye test
  (18.5, 5.5, 1),
  #(18.5, 11.5, 1),
  (18.5, 12.5, 1),
  
  #some barrels around the map
  (21.5, 1.5, 0),
  (15.5, 1.5, 0),
  (16.0, 1.8, 0),
  (16.2, 1.2, 0),
  (3.5,  2.5, 0),
  (9.5, 15.5, 0),
  (10.0, 15.1,0),
  (10.5, 15.8,0),
]

def load_image(image, darken, colorKey = None):
    ret = []
    if colorKey is not None:
        image.set_colorkey(colorKey)
    if darken:
        image.set_alpha(127)
    for i in range(image.get_width()):
        s = pygame.Surface((1, image.get_height())).convert()
        #s.fill((0,0,0))
        s.blit(image, (- i, 0))
        if colorKey is not None:
            s.set_colorkey(colorKey)
        ret.append(s)
    return ret

def main():
  
    t = time.perf_counter() #time of current frame
    oldTime = 0. #time of previous frame
    pygame.mixer.init()
    pygame.mixer.music.load("MuseUprising.mp3")
    # pygame.mixer.music.play(-1)
    size = w, h = 1280,720
    pygame.init()
    window = pygame.display.set_mode(size)
    pygame.display.set_caption("Wolfy_3D_Example")
    screen = pygame.display.get_surface()
    #pixScreen = pygame.surfarray.pixels2d(screen)
    pygame.mouse.set_visible(False)
    clock = time.perf_counter()
    
    f = pygame.font.SysFont(pygame.font.get_default_font(), 20)
    
    wm = worldManager.WorldManager(worldMap,sprite_positions, 20, 11.5, -1, 0, 0, .66)
    
    weapons = [Weapon("fist"),
               Weapon("pistol"),
               Weapon("shotgun"),
               Weapon("dbshotgun"),
               Weapon("chaingun"),
               Weapon("plasma"),
               Weapon("rocket"),
               Weapon("bfg"),
               Weapon("chainsaw")
               ]
    weapon_numbers = [K_1,K_2,K_3,K_4,K_5,K_6,K_7,K_8,K_0]
    weapon = weapons[0]
    
    testclock = pygame.time.Clock()
    
    while(True):
        testclock.tick(60)
        
        wm.draw(screen)
        
        
        # timing for input and FPS counter
        
        frameTime = float(testclock.get_time()) / 1000.0 # frameTime is the time this frame has taken, in seconds
        # t = time.Clock()
        #text = f.render(str(testclock.get_fps()), False, (255, 255, 0))
        #screen.blit(text, text.get_rect(), text.get_rect())
        weapon.draw(screen, testclock)
        pygame.display.flip()

        # speed modifiers
        moveSpeed = frameTime * 12.0 # the constant value is in squares / second
        rotSpeed = frameTime * 2.0 # the constant value is in radians / second
        
        for event in pygame.event.get(): 
            if event.type == QUIT: 
                return False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
                    pygame.quit()
                elif event.key == K_SPACE:
                    #shoot
                    #weapon.play()
                    print("camera x: " + str(wm.camera.x))
                    print("camera y: " + str(wm.camera.y))
                    print("camera px: " + str(wm.camera.planex))
                    print("camera py: " + str(wm.camera.planey))
                elif event.key in weapon_numbers:
                    weapon.stop()
                    weapon = weapons[weapon_numbers.index(event.key)]
            elif event.type == KEYUP:
                if event.key == K_SPACE:
                    weapon.stop()
            else:
                pass 
        
        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            # move forward if no wall in front of you
            
            # Move forward and back on z-axis
            # Get the move value
            moveX = wm.camera.x + wm.camera.dirx * moveSpeed
            
            # Move only if not collided with a wall
            if worldMap[int(moveX)][int(wm.camera.y)]==0:
                wm.camera.x += wm.camera.dirx * moveSpeed
            
            # Move forward and back on x-axis or y
            # Get the move value
            moveY = wm.camera.y + wm.camera.diry * moveSpeed

            # Only move if not collided with a wall
            if worldMap[int(wm.camera.x)][int(moveY)]==0:
                wm.camera.y += wm.camera.diry * moveSpeed
        if keys[K_DOWN]:
            # move backwards if no wall behind you
            if(worldMap[int(wm.camera.x - wm.camera.dirx * moveSpeed)][int(wm.camera.y)] == 0):
                wm.camera.x -= wm.camera.dirx * moveSpeed
                
            if(worldMap[int(wm.camera.x)][int(wm.camera.y - wm.camera.diry * moveSpeed)] == 0):
                wm.camera.y -= wm.camera.diry * moveSpeed
        if (keys[K_RIGHT] and not keys[K_DOWN]) or (keys[K_LEFT] and keys[K_DOWN]):
            # rotate to the right
            # both camera direction and camera plane must be rotated
            oldDirX = wm.camera.dirx
            wm.camera.dirx = wm.camera.dirx * math.cos(- rotSpeed) - wm.camera.diry * math.sin(- rotSpeed)
            wm.camera.diry = oldDirX * math.sin(- rotSpeed) + wm.camera.diry * math.cos(- rotSpeed)
            oldPlaneX = wm.camera.planex
            wm.camera.planex = wm.camera.planex * math.cos(- rotSpeed) - wm.camera.planey * math.sin(- rotSpeed)
            wm.camera.planey = oldPlaneX * math.sin(- rotSpeed) + wm.camera.planey * math.cos(- rotSpeed)
        if (keys[K_LEFT] and not keys[K_DOWN]) or (keys[K_RIGHT] and keys[K_DOWN]): 
            # rotate to the left
            # both camera direction and camera plane must be rotated
            oldDirX = wm.camera.dirx
            wm.camera.dirx = wm.camera.dirx * math.cos(rotSpeed) - wm.camera.diry * math.sin(rotSpeed)
            wm.camera.diry = oldDirX * math.sin(rotSpeed) + wm.camera.diry * math.cos(rotSpeed)
            oldPlaneX = wm.camera.planex
            wm.camera.planex = wm.camera.planex * math.cos(rotSpeed) - wm.camera.planey * math.sin(rotSpeed)
            wm.camera.planey = oldPlaneX * math.sin(rotSpeed) + wm.camera.planey * math.cos(rotSpeed)
            
    pygame.quit()

fps = 8
class Weapon(object):
    
    def __init__(self, weaponName="shotgun", frameCount = 5):
        self.images = []
        self.loop = False
        self.playing = False
        self.frame = 0
        self.oldTime = 0
        for i in range(frameCount):
            img = pygame.image.load("pics/weapons/%s%s.bmp" % (weaponName, i+1)).convert()
            img = pygame.transform.scale2x(img)
            img = pygame.transform.scale2x(img)
            img.set_colorkey(img.get_at((0,0)))
            self.images.append(img)
    def play(self):
        self.playing = True
        self.loop = True
    def stop(self):
        self.playing = False
        self.loop = False
    def draw(self, surface, time):
        # if(self.playing or self.frame > 0):
            # if(time.get_fps() > (self.oldTime + (1.0/fps))):
                # self.frame = (self.frame+1) % len(self.images)
                # if self.frame == 0: 
                    # if self.loop:
                        # self.frame = 1
                    # else:
                        # self.playing = False
                        
                #self.oldTime = time
        img = self.images[self.frame]
        surface.blit(img, (surface.get_width()/2 - img.get_width()/2, surface.get_height()-img.get_height()))
            
if __name__ == '__main__':
    main()
    pygame.quit()
