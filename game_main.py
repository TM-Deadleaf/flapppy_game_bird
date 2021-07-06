import pygame #for making games
import random #for generating random numbers  
import sys # for exit the game
from pygame.locals import *



#global variables

FPS=32
SCREENWIDTH=289
SCREENHEIGHT=511 
SCREEN=pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))#initialize the game window
GROUNDY=SCREENHEIGHT * 0.8
GAME_SOUNDS={}
GAME_SPRITES={}
PLAYER='misc/images/bird.png'
BACKGROUND='misc/images/background.png'
PIPE='misc/images/pipe.png'


def welcomeScreen():
    """
    shows welcome image
    """
    playerx=int(SCREENWIDTH/5) #gives pos of the bird in x axis
    playery=int((SCREENHEIGHT-GAME_SPRITES['player'].get_height())/2) #gives pos of the bird form y axis 
    messagex=int((SCREENWIDTH-GAME_SPRITES['message'].get_height())/0.42)
    messagey=int(SCREENHEIGHT * 0.13)
    basex=0
    while True:
        for event in pygame.event.get():#for every event eg.keyboard and mouse clicks
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE ):
                pygame.quit()
                sys.exit()
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                return #return to the mainGame() function
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0,))
                SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
                SCREEN.blit(GAME_SPRITES['message'],(messagex,messagey))
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def mainGame():
    score=0
    playerx=int(SCREENWIDTH/5)
    playery=int(SCREENWIDTH/2)
    basex=0
    newPipe1=randomPipe() #create  pipes randomly 
    newPipe2=randomPipe()
    #upper pipes
    upperPipes=[
        {'x':SCREENWIDTH+200,'y':newPipe1[0]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2),'y':newPipe2[0]['y']}
    ]
    #lower pipes
    lowerPipes=[
        {'x':SCREENWIDTH+200,'y':newPipe1[1]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/5),'y':newPipe2[1]['y']}
    ]

    pipeVelx=-4

    playerVelY=-9
    playerMaxVelY=10
    playerMinVelY=-8
    playerAccY=1

    playerFlapAccv=-8 # velocity while flapping
    playerFlaped=False # true only when bird is flying

    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                if playery>0:
                    playerVelY=playerFlapAccv
                    playerFlaped=True
                    GAME_SOUNDS['wing'].play()
        crashTest=isCollide(playerx,playery,upperPipes,lowerPipes)
        if crashTest:
            return
        #check for score
        playermidpos=playerx+GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipemidpos=pipe['x']+GAME_SPRITES['pipe'][0].get_width()/2
            if pipemidpos<=playermidpos < pipemidpos +4:
                score+=1
                print("your score is {}".format(score))
                GAME_SOUNDS['point'].play()
        if playerVelY <playerMaxVelY and not playerFlaped:
            playerVelY+=playerAccY
        
        if playerFlaped:
            playerFlaped=False
        playerHeight=GAME_SPRITES['player'].get_height()
        playery=playery+ min(playerVelY,GROUNDY-playery-playerHeight)

        #pipes to the left
        for upperPipe,lowerPipe in zip(upperPipes,lowerPipes):
            upperPipe['x']+=pipeVelx
            lowerPipe['x']+=pipeVelx
        if 0<upperPipes[0]['x']<5:
            newpipe=randomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])
        
        #removing pipe
        if upperPipes[0]['x']< -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        #blits images

        SCREEN.blit(GAME_SPRITES['background'],(0,0))
        for upperPipe,lowerPipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperPipe['x'],upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerPipe['y'],lowerPipe['y']))
        SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
        myDigits=[int(x) for x in list(str(score))]
        width=0
        for digit in myDigits:
            width+=GAME_SPRITES['numbers'][digit].get_width()
            Xoffset=(SCREENWIDTH-width)/2
        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit],(Xoffset,SCREENHEIGHT*0.12))
            Xoffset+=GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
def isCollide(playerx,playery,upperPipes,lowerPipes):
    if playery> GROUNDY - 25  or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False
    

def randomPipe():
    """
    generate positions of  the pipes
    """
    pipeHeight=GAME_SPRITES['pipe'][0].get_height()
    offset=SCREENHEIGHT/3
    y2=offset+random.randrange(0,int(SCREENHEIGHT-GAME_SPRITES['base'].get_height()- 1.2 *offset))
    pipex=SCREENWIDTH + 10
    y1=pipeHeight-y2+offset
    pipe=[
        {'x':pipex,'y':-y1},
        {'x':pipex,'y':y2}
    ]
    return pipe

















if __name__ == '__main__':
    #driver function
    pygame.init() 
    FPSCLOCK=pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')
    GAME_SPRITES['numbers']=(
        pygame.image.load('misc/images/0.png').convert_alpha(),
        pygame.image.load('misc/images/1.png').convert_alpha(),
        pygame.image.load('misc/images/2.png').convert_alpha(),
        pygame.image.load('misc/images/3.png').convert_alpha(),
        pygame.image.load('misc/images/4.png').convert_alpha(),
        pygame.image.load('misc/images/5.png').convert_alpha(),
        pygame.image.load('misc/images/6.png').convert_alpha(),
        pygame.image.load('misc/images/7.png').convert_alpha(),
        pygame.image.load('misc/images/8.png').convert_alpha(),
        pygame.image.load('misc/images/9.png').convert_alpha(),
    ) #dict where key numbers are initialized

    GAME_SPRITES['message']=pygame.image.load('misc/images/message.png').convert_alpha()
    GAME_SPRITES['base']=pygame.image.load('misc/images/base.png').convert_alpha()
    GAME_SPRITES['pipe']=(
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
        pygame.image.load(PIPE).convert_alpha()
    ) #dict key pipe having a tuple of two pipes inverted each other

    #game sounds
    GAME_SOUNDS['die']=pygame.mixer.Sound('misc/sounds/die.wav')
    GAME_SOUNDS['hit']=pygame.mixer.Sound('misc/sounds/hit.wav')
    GAME_SOUNDS['point']=pygame.mixer.Sound('misc/sounds/point.wav')
    GAME_SOUNDS['swoosh']=pygame.mixer.Sound('misc/sounds/swoosh.wav')
    GAME_SOUNDS['wing']=pygame.mixer.Sound('misc/sounds/wing.wav')


    GAME_SPRITES['background']=pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player']=pygame.image.load(PLAYER).convert_alpha()


    while True:
        welcomeScreen() #welcome screen until exits
        mainGame() #main game driver
