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

# Constant values for sprite images

LIGHT_IMAGE = 2
PILLAR_IMAGE = 1
BARREL_IMAGE = 0

####  WALL TEXTURES   #####
# 8 - Colourstone
# 7 - Wood
# 6 - Mossy
# 5 - Bluestone
# 4 - Greystone
# 3 - Redbrick
# 2 - Purplestone
# 1 - Eagle

WALL_TEX_COLOURSTONE = 8
WALL_TEX_WOOD = 7
WALL_TEX_MOSSY = 6

worldMap =[
 [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
 [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
 [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
 [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
 [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
 [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
 [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
 [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
 [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
 [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
 [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
 [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
 [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
 [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
 [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
 [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
 [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
 [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
 [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
 [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
 [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
 [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
 [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
];

sprite_positions=[]

# Add sprite to collection
def add_sprite(zposin, xposin, image):
    sprite_positions.append([zposin, xposin, image])  

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
    
def build_world_add_sprites():
    # Add a Pillar to each corner of the game scene
    
    # Back wall left
    add_sprite(21.5, 1.5, PILLAR_IMAGE)    
    
    # Back wall right
    add_sprite(21.5, 22.5, PILLAR_IMAGE)
    
    # Front Wall Right
    add_sprite(1.5, 22.5, PILLAR_IMAGE)
    
    # Front Wall Left
    add_sprite(1.5, 1.5, PILLAR_IMAGE)
    
    # Add some barrels to the game scene
    add_sprite(10.0, 10.0, BARREL_IMAGE)
    add_sprite(10.0, 12.0, BARREL_IMAGE)
    add_sprite(10.0, 14.0, BARREL_IMAGE)

# A function to detect     
def spriteCollision(currentPositionIn, projectedPosition):
    # Returns True if collision, Fale if no collision
    retValue = False # Return False by default
    
    # Get Player position
    player_x_pos = currentPositionIn[0]
    player_y_pos = currentPositionIn[1]
    
    # Get Camera direction 
    player_cam_dirx = currentPositionIn[2]
    player_cam_diry = currentPositionIn[3]
    
    
    for sprite in sprite_positions:
        # Extract sprite details
        sprite_x_pos = sprite[0]
        sprite_y_pos = sprite[1]
        sprite_type = sprite[2]
        
        # Collision detection on approach to barrels
        if player_x_pos <= (sprite_x_pos+1.0) and player_y_pos >= (sprite_y_pos-0.2) and player_y_pos <= (sprite_y_pos+0.2) and sprite_type == BARREL_IMAGE and player_cam_dirx < 0.0:
            retValue = True
        else:            
            # Collision detection on return from barrels
            if player_x_pos >= (sprite_x_pos-2.0) and player_y_pos >= (sprite_y_pos-0.2) and player_y_pos <= (sprite_y_pos+0.2) and sprite_type == BARREL_IMAGE and player_cam_dirx > 0.0:
                retValue = True
        
    return retValue
        
        
    
    

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
    
    # Game Scene setup
    build_world_add_sprites()
    
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
                    print("camera dirx: " + str(wm.camera.dirx))
                    print("camera diry: " + str(wm.camera.diry))
                    
                    print(sprite_positions[4][0])
                    print(sprite_positions[4][1])
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
                # Collision Detection with game sprites
                spriteCollisionDet = spriteCollision([wm.camera.x, wm.camera.y, wm.camera.dirx, wm.camera.diry], moveX)
                if spriteCollisionDet == False:
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
