import cv2
import os
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

imgbackground = cv2.imread('Resources/Background.png')

#IMPORTING ALL THE MODE IMAGES TO A  LIST
#creating a list of Modes folder to change them dynamically
folderpathModes = 'Resources/Modes'
print(os.listdir(folderpathModes))
listImgModesPath = os.listdir(folderpathModes) # contains the path of modes floder as string
listImgModes = []
#filling Modes images in list
for imgMode in listImgModesPath:
    listImgModes.append( cv2.imread(os.path.join(folderpathModes,imgMode)))
    print(listImgModes)

#IMPORTING ALL THE ICONS TO A LIST
folderpathIcons = 'Resources/Icons'
print(os.listdir(folderpathModes))
listImgIconsPath = os.listdir(folderpathIcons) # contains the path of icons floder as string
listImgIcons = []
#filling icon images in list
for imgIconspath in listImgIconsPath:
    listImgIcons.append( cv2.imread(os.path.join(folderpathIcons,imgIconspath)))
    print(listImgIcons)


Modetype = 0  #  changing the selection Modes images on o/p
selection = -1 # finger selection ctr
counter = 0 # for time delay in selection
selectionspeed = 10# multiplier for ellipse speed
modeposition = [(1136,196),(1000,384),(1136,581)] # center positions of mode images 1,2,3 options
counterpause = 0 # for delay in next selection, to let customer think about order
SelectionList = [-1,-1,-1] # storing order icons

detector = HandDetector(detectionCon=0.8, maxHands=1) # 

while True:
    success,img = cap.read()

      # Find the hand and its landmarks
    hands, img = detector.findHands(img) 

    #overlaying the webcam feed on the background image height,width
    imgbackground[139:139+480,50:50+640]=img

     #overlaying the selection images on the background image height,width
    imgbackground[0:720,847:1280]=listImgModes[Modetype]

     # Find the hand and its landmarks
    hands, img = detector.findHands(img) 



# selection is done here ...

    # if couterpause is 0 that is delay in selecting next item, and modetype list's 3rd index has last image so to 
    # not select afterwards  it is <3
    if hands and counterpause == 0 and Modetype<3:
            # Hand 1
            hand1 = hands[0]
            fingers1 = detector.fingersUp(hand1) # checks how many fingers are up
            print(fingers1)

            if fingers1 == [0,1,0,0,0]:# if index finger detected change counter and selection to 1 
                if selection != 1:
                    counter =1
                selection = 1

            elif fingers1 == [0,1,1,0,0]:# if index finger detected change counter and selection to 2
                if selection != 2:
                    counter =1
                selection = 2

            elif fingers1 == [0,1,1,1,0]:# if index finger detected change counter and selection to 2 
                if selection != 3:
                    counter =1
                selection = 3

            else:
                selection = -1
                counter =0
            
            # if finger is up  then we'll increase the counter
            if counter>0:
                counter+=1
                print(counter)
                # an ellipse is an fuction in opencv that will allow us to create a variable arc
                # it will go round and round and finally selects objects    
                cv2.ellipse(imgbackground,modeposition[selection-1],(103,103),0,0,counter*selectionspeed,(0,255,0),20)
                
                if counter*selectionspeed>360: # it works when selection is completed
                    SelectionList[Modetype] = selection 
                    Modetype+=1 
                    counter = 0
                    selection = -1
                    counterpause = 1
    
    # once the selection is done, and now counterpause =1 ,make the next selection  delay some time
    if counterpause>0:
        counterpause+=1
        if counterpause>60: #since frame rate is 30fps , then 60 means 2 sec delay for next selection
            counterpause =0

    # ADD SELECTION ITEM AT THE BOTTOM
    if SelectionList[0] != -1:
        imgbackground[636:636+65,133:133+65] = listImgIcons[SelectionList[0] - 1]
    
    if SelectionList[1] != -1:
        imgbackground[636:636+65,340:340+65] = listImgIcons[SelectionList[0] + 2]
    
    if SelectionList[2] != -1:
        imgbackground[636:636+65,542:542+65] = listImgIcons[SelectionList[0] + 5]



    #Displaying 
   # cv2.imshow("Image",img), for webcam only
    cv2.imshow("B.TECH CHAI WALA",imgbackground)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break