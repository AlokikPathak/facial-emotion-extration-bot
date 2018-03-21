#Check the mood of the user.

import argparse
import base64
import json

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

def main():
    
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials)

    with open('2.jpg', 'rb') as image:
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
        print 'You seem ',response['responses'][0]['faceAnnotations'][0]['angerLikelihood'],' to be angry and ',response['responses'][0]['faceAnnotations'][0]['joyLikelihood'],' to be happy.'
        #print json.dumps(response, indent=4, sort_keys=True)	#Print it out and make it somewhat pretty.

if __name__ == '__main__':

    main()