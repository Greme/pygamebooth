import pygame
import os
import io
import PIL
import sys
import picamera

from pygame.locals import *
from PIL import Image
from PIL import ImageOps

##########Folder storage stuff#########
tempStorage = "/home/pi/testpicamGUI/pygamecam/tempPhoto/"
archiveStorage = "/home/pi/testpicamGUI/pygamecam/allPhotos/"
photoMask  = "/home/pi/testpicamGUI/pygamecam/photomask_white.png"
maskImg = Image.open(photoMask)

##########init pycamera stuff #########
STILL_RESOLTUION = (3280,2464)
CAMERA_SHUTTER_DENOM = 100

CAM_SPEED = int((1.0 / float(CAMERA_SHUTTER_DENOM)) * 1000000.0)

camera = picamera.PiCamera()
camera.resolution = STILL_RESOLTUION

camera.shutter_speed = CAM_SPEED
print CAM_SPEED
##########init pygame stuff#####
pygame.init() #Initialise pygame

## Main program loop!
mainRunning = True
## Keeps Track of when photo process is running so that it cant be restarted halfway through and break everything....
photosRunning = False


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PREVIEW_WIDTH = 768
PREVIEW_HEIGHT = 576
CAM_ALPHA =200

pygame.mixer.pre_init(44100, -16, 1, 1024*3) #PreInit Music, plays faster
infoObject = pygame.display.Info() ## dont need this now as fixing to 1080p
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.FULLSCREEN) #Full screen 640x480
timersurface =  pygame.Surface((SCREEN_WIDTH, 200))
background = pygame.Surface(screen.get_size()) #Create the background object
background = background.convert() #Convert it to a background
bgImage = pygame.image.load("resize_pb_background.png")
background.blit(bgImage, (0,0))
screen.blit(background, (0,0))
pygame.display.flip()

### Styling var - like location of text, numbers, fonts etc!
NUMBER_CENTER = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
TEXT_CENTER = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
messageFont = pygame.font.SysFont("Arial",72)
numberFont = pygame.font.SysFont("Impact",200)

def showInterstitial(text):
    screen.blit(background, (0,0))
    messageText = messageFont.render(text, True, (255,255,255))
    text_Rect = messageText.get_rect(center=TEXT_CENTER)
    screen.blit(messageText, text_Rect)
    pygame.display.flip()
    pygame.time.wait(1000)

def countDownPicture(imageNumber, timeStamp):
    global photosRunning
    photosRunning = True

    #Reset background
    screen.blit(background, (0,0))

    countdownText = messageFont.render("Get Ready!", True, (255,255,255))
    text_Rect = countdownText.get_rect(center=TEXT_CENTER)
    screen.blit(countdownText, text_Rect)
    pygame.display.flip()
    screen.fill((255,255,255), ((infoObject.current_w / 2) - ((PREVIEW_WIDTH + 8) / 2),(infoObject.current_h / 2) - ((PREVIEW_HEIGHT +8) / 2),PREVIEW_WIDTH+8,PREVIEW_HEIGHT+8))
    screen.fill((0,0,0), ((infoObject.current_w / 2) - (PREVIEW_WIDTH / 2),(infoObject.current_h / 2) - (PREVIEW_HEIGHT / 2),PREVIEW_WIDTH,PREVIEW_HEIGHT))
    pygame.time.wait(1500)
    pygame.display.flip()
    #pygame.draw.rect(screen, (255,255,255), ((infoObject.current_w / 2) - (PREVIEW_WIDTH / 2),(infoObject.current_h / 2) - (PREVIEW_HEIGHT / 2),PREVIEW_WIDTH,PREVIEW_HEIGHT),4)
    #pygame.draw.rect(screen, (0,0,0), ((infoObject.current_w / 2) - (PREVIEW_WIDTH / 2),(infoObject.current_h / 2) - (PREVIEW_HEIGHT / 2),PREVIEW_WIDTH,PREVIEW_HEIGHT))
    camera.start_preview(alpha=CAM_ALPHA,fullscreen=False, window = ((infoObject.current_w / 2) - (PREVIEW_WIDTH / 2),(infoObject.current_h / 2) - (PREVIEW_HEIGHT / 2),PREVIEW_WIDTH,PREVIEW_HEIGHT))
    pygame.time.wait(1000)

    numberText = numberFont.render("3", True, (255,128,128))
    number_Rect = numberText.get_rect(center = NUMBER_CENTER)
    screen.fill((0,0,0),text_Rect)
    screen.fill((0,0,0), number_Rect)
    screen.blit(numberText, number_Rect)
    pygame.display.flip()
    pygame.time.wait(1500)

    numberText = numberFont.render("2", True, (255,128,128))
    screen.fill((0,0,0),number_Rect)
    number_Rect = numberText.get_rect(center = NUMBER_CENTER)
    screen.blit(numberText, number_Rect)
    pygame.display.flip()
    pygame.time.wait(1500)
    
    numberText = numberFont.render("1", True, (255,128,128))
    screen.fill((0,0,0),number_Rect)
    number_Rect = numberText.get_rect(center = NUMBER_CENTER)
    screen.blit(numberText, number_Rect)
    pygame.display.flip()
    pygame.time.wait(1500)    

    screen.fill((0,0,0),number_Rect)
    pygame.display.flip()

    camera.capture(tempStorage + timeStamp +'_' + str(imageNumber)+'.jpg')
    camera.stop_preview()

    pictureTaken = pygame.image.load(tempStorage + timeStamp +'_' + str(imageNumber)+'.jpg')
    pictureTaken = pygame.transform.scale(pictureTaken,(PREVIEW_WIDTH,PREVIEW_HEIGHT))
    screen.blit(pictureTaken, ((infoObject.current_w / 2) - (PREVIEW_WIDTH / 2),(infoObject.current_h / 2) - (PREVIEW_HEIGHT / 2)))
    ##Maybe add a random message here...!
    pygame.display.flip()    

    photosRunning = False



while mainRunning:
    takePictures = False
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainRunning = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainRunning = False
                if (event.key == pygame.K_HASH) and (not photosRunning):
                    takePictures = True
                else:
                    pass
                    
    except KeyboardInterrupt:
	    mainRunning = False


    if takePictures:
        startTime = time.strftime('%Y%m%d%H%M%S')

        ## Take first picture
        countDownPicture(1,startTime)
        pygame.time.wait(2000)

        ## Clear image and show interstitial
        showInterstitial("And number two...")

        ## Take second picture
        countDownPicture(2,startTime)
        pygame.time.wait(2000)
        print camera.exposure_speed

        ## Clear image and show interstitial
        showInterstitial("And finally...")

        ## Take last picture
        countDownPicture(3,startTime)
        pygame.time.wait(2000)

        ## Composite!
        baseImg = Image.new('RGBA',(1800,1200),(255,255,255))
        photoOne = ImageOps.autocontrast(Image.open(tempStorage + startTime +'_1.jpg').resize((900,600),resample=PIL.Image.ANTIALIAS))
        photoTwo = ImageOps.autocontrast(Image.open(tempStorage + startTime +'_2.jpg').resize((900,600),resample=PIL.Image.ANTIALIAS))
        photoThree = ImageOps.autocontrast(Image.open(tempStorage + startTime +'_3.jpg').resize((900,600),resample=PIL.Image.ANTIALIAS))

        baseImg.paste(photoOne,(0,0))
        baseImg.paste(photoTwo,(900,0))
        baseImg.paste(photoThree,(0,600))
        finalImg = Image.alpha_composite(baseImg,maskImg)
        finalImg.save(tempStorage + startTime + "_comp.jpg", dpi=(300,300))
        
                
        ## Clear event log to stop "chaining" photographs!
        pygame.event.clear()
        screen.blit(background, (0,0))
        pygame.display.flip()
        
        
pygame.quit()
sys.exit()
