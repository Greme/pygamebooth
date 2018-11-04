import pygame
import io
import PIL
import sys
import picamera
import requests
import piwigo
import time
import subprocess
import RPi.GPIO as GPIO

from pygame.locals import *
from PIL import Image
from PIL import ImageOps

##########Folder storage stuff#########
installationLocation = "/home/pi/testpicamGUI/pygamecam/"
tempStorage = "/home/pi/testpicamGUI/pygamecam/tempPhoto/"
archiveStorage = "/home/pi/testpicamGUI/pygamecam/allPhotos/"
photoMask  = installationLocation + "photomask_white.png"
maskImg = Image.open(photoMask)

##########init pycamera stuff #########
STILL_RESOLTUION = (3280,2464)
CAMERA_SHUTTER_DENOM = 100

CAM_SPEED = int((1.0 / float(CAMERA_SHUTTER_DENOM)) * 1000000.0)

camera = picamera.PiCamera()
camera.resolution = STILL_RESOLTUION

camera.shutter_speed = CAM_SPEED
print CAM_SPEED
stream = io.BytesIO()

##########init GPIO stuff for light ##########
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
GPIO.output(12, GPIO.HIGH)


##########init pygame stuff#####
pygame.init() #Initialise pygame
mainClock = pygame.time.Clock()

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

def displayMessage(text):
    messageText = messageFont.render(text, True, (255,255,255))
    text_Rect = messageText.get_rect(center=TEXT_CENTER)
    screen.blit(messageText, text_Rect)
    pygame.display.flip()

def showInterstitial(text):
    screen.blit(background, (0,0))
    displayMessage(text)
    pygame.time.wait(1000)

def piwigoUpload(imageLocs, cat):
    photoSite = piwigo.Piwigo('http://samandgraemewedding.co.uk/piwigo')
    photoSite.pwg.session.login(username='egcyf', password='bigvegPIWIGO10')
    for imageLoc in imageLocs:
        photoSite.pwg.images.addSimple(image=imageLoc, category=cat)
    photoSite.pwg.session.logout()
    print "Upload complete!"

def countDownPicture():
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
    GPIO.output(12, GPIO.LOW)
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
    camera.capture(stream, format='jpeg')
    camera.stop_preview()
    stream.seek(0)
    screen.fill((0,0,0),number_Rect)
    pygame.display.flip()
    GPIO.output(12, GPIO.HIGH)
    
    previewImage = Image.open(stream).resize((PREVIEW_WIDTH,PREVIEW_HEIGHT),resample=PIL.Image.ANTIALIAS)
    imageSize = previewImage.size
    print imageSize
    screen.blit(pygame.image.fromstring(previewImage.tostring("raw","RGB"),imageSize,"RGB"), ((infoObject.current_w / 2) - (PREVIEW_WIDTH / 2),(infoObject.current_h / 2) - (PREVIEW_HEIGHT / 2)))
    ##Maybe add a random message here...!
    pygame.display.flip()    
    stream.seek(0)
    fullImage = ImageOps.autocontrast(Image.open(stream))
    stream.seek(0)
    
    photosRunning = False
    return fullImage


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
        photoOne = countDownPicture()
        pygame.time.wait(2000)

        ## Clear image and show interstitial
        showInterstitial("And number two...")

        ## Take second picture
        photoTwo = countDownPicture()
        pygame.time.wait(2000)

        ## Clear image and show interstitial
        showInterstitial("And finally...")

        ## Take last picture
        photoThree = countDownPicture()
        pygame.time.wait(2000)

        ## Composite!
        screen.blit(background, (0,0))
        displayMessage("Compositing...")
        baseImg = Image.new('RGBA',(1800,1200),(255,255,255))
        baseImg.paste(photoOne.resize((900,600),resample=PIL.Image.ANTIALIAS),(0,0))
        baseImg.paste(photoTwo.resize((900,600),resample=PIL.Image.ANTIALIAS),(900,0))
        baseImg.paste(photoThree.resize((900,600),resample=PIL.Image.ANTIALIAS),(0,600))
        finalImg = Image.alpha_composite(baseImg,maskImg)

        screen.blit(background, (0,0))
        displayMessage("Done!")
        previewFinal = finalImg.resize((PREVIEW_WIDTH,PREVIEW_HEIGHT),resample=PIL.Image.ANTIALIAS)
        screen.blit(pygame.image.fromstring(previewFinal.tostring("raw","RGB"),(PREVIEW_WIDTH,PREVIEW_HEIGHT),"RGB"), ((infoObject.current_w / 2) - (PREVIEW_WIDTH / 2),(infoObject.current_h / 2) - (PREVIEW_HEIGHT / 2)))

        #Backup screen view to redisplaying later
        screenBackup = screen
        pygame.display.flip()
        mainClock.tick()
        displayMessage("Saving images...")

        ## Save originals and base image :)
        finalImg.save(archiveStorage + startTime + "_comp.jpg", dpi=(300,300))
        photoOne.save(archiveStorage + startTime + "_1.jpg", dpi=(300,300))
        photoTwo.save(archiveStorage + startTime + "_2.jpg", dpi=(300,300))
        photoThree.save(archiveStorage + startTime + "_3.jpg", dpi=(300,300))

        screen.blit(screenBackup, (0,0))
        displayMessage("Uploading images...")
##        ##Upload them - NB: TAKES TOO LONG, CHANGE BELOW TO SUBPROCESS TO FIRE AND FORGET!
##        piwigoUpload([archiveStorage + startTime + "_comp.jpg"], 2)
##        piwigoUpload([archiveStorage + startTime + "_1.jpg",archiveStorage + startTime + "_2.jpg",archiveStorage + startTime + "_3.jpg"],3)

        uploadDict = {3:[],2:[]}
        uploadDict[3].append(archiveStorage + startTime + "_1.jpg")
        uploadDict[3].append(archiveStorage + startTime + "_2.jpg")
        uploadDict[3].append(archiveStorage + startTime + "_3.jpg")
        uploadDict[2].append(archiveStorage + startTime + "_comp.jpg")
        uploadArgs = ["python", installationLocation + "piwigouploader.py",''+str(uploadDict)+'']
        subprocess.Popen(uploadArgs)
        
        mainClock.tick()
        #Wait some more time if image hasnt been shown longer than 4seconds
        pygame.time.wait(max(4000-mainClock.get_time(),0))

        ## Clear event log to stop "chaining" photographs!
        pygame.event.clear()
        screen.blit(background, (0,0))
        pygame.display.flip()
        
        
pygame.quit()
sys.exit()
