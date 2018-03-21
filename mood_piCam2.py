#Check the mood of the user.

import argparse
import base64
import json
import picamera

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

camera = picamera.PiCamera(resolution=(480, 320))
camera.vflip = True
camera.hflip = True

def snap():
    
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials)

    camera.capture('image.jpg')    #captures the image from the camera & save it as 2.jpg

    with open('image.jpg', 'rb') as image:   #reading the file as ImageFile
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(body={
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [{
                    'type': 'FACE_DETECTION',
                    'maxResults': 10
                }]
            }]
        })
        response = service_request.execute() 
	
        #print response

        print 'You seems...\n',response['responses'][0]['faceAnnotations'][0]['joyLikelihood'],' to be HAPPY..!,\n',response['responses'][0]['faceAnnotations'][0]['angerLikelihood'],' to be ANGRY..!\n',response['responses'][0]['faceAnnotations'][0]['surpriseLikelihood'],' to be Surprised..!\n',response['responses'][0]['faceAnnotations'][0]['sorrowLikelihood'],' to be SORROW..!,\n',response['responses'][0]['faceAnnotations'][0]['underExposedLikelihood'],' to be UnderExpossed..!,\n',response['responses'][0]['faceAnnotations'][0]['blurredLikelihood'],' to be Blurred..!,\n',response['responses'][0]['faceAnnotations'][0]['headwearLikelihood'],' to be Head Wear..!,\n\n'

	#   Printing Final Expression After Analysis of All Results
	C=['VERY_LIKELY','LIKELY','POSSIBLE']
	E=['joyLikelihood','angerLikelihood','surpriseLikelihood','sorrowLikelihood','underExposedLikelihood','blurredLikelihood','headwearLikelihood']
	F=['Happy','Angry','Surprised','Sad','Unexplored','Blurred','Headwear']
	
	flag = True
	for i in range(0,3):
    		for j in range(0,5):
        		if C[i]==response['responses'][0]['faceAnnotations'][0][E[j]]: 
				print'Final Expression:'
            			print 'You seems',response['responses'][0]['faceAnnotations'][0][E[j]],' ',F[j],'...!'
            			flag=False
				break  #if any emotion is VERY_LIKELY, LIKELY OF POSSIBLE

	if(flag==True):
    		print('You seems Normal')	

        
	#print json.dumps(response, indent=4, sort_keys=True)	#Print it out and make it somewhat pretty.

while 1:
	if(raw_input("Click y for SNAP..! and any other for exit: ")=="y"):
		snap()
	else:
		exit()