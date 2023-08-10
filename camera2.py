import cv2
import mediapipe as mp
import numpy as np
#import itertools
from time import time
#import matplotlib.pyplot as plt

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
#mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose
def calculate_angle(a,b,c):
        a = np.array(a) # First
        b = np.array(b) # Mid
        c = np.array(c) # End
    
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
    
        if angle >180.0:
            angle = 360-angle
        
        return angle 


counter = 0 
stage = None
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    

    def get_frame(self):
        
        ret, frame =self.video.read()
        # Curl counter variables
        global counter 
        global stage 
        
        ## Setup mediapipe instance
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose: 
           # while self.video.isOpened():
              #  ret, frame = self.video.read()


    
    
                # Flip the image horizontally for a selfie-view display.
                #cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
        
                # Recolor image to RGB
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
      
                # Make detection
                results = pose.process(image)
    
                # Recolor back to BGR
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                # Render detections
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                 )        
        
                # Extract landmarks
                try:
                    landmarks = results.pose_landmarks.landmark
            
            
                # Get coordinates of left joints
                    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            
            
                        
                    #get hight of LEFTjoints
                    y_scoodinate = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    y_ecoodinate = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]


                    #get coordinates of right points
                    #rshoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    #relbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                    #rwrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                    #y_rscoodinate = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    #y_recoodinate = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                    # Calculate angle
                    angle = calculate_angle(shoulder, elbow, wrist)
                    
            
            
                    # Visualize angle
                    cv2.putText(image, str(angle), 
                           tuple(np.multiply(elbow, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            
                    # Curl counter logic
                    #if shoulder>elbow:
            
                    if y_scoodinate>y_ecoodinate :# or y_rscoodinate>y_recoodinate :
                        if angle > 160 :
                            stage = "Up"
                            print(counter)
                            print("elbow    :",y_ecoodinate)
                            print("shoulder :",y_scoodinate)
                            print(stage)  
                    #if shoulder>elbow:
                    elif y_scoodinate<y_ecoodinate :# or y_rscoodinate<y_recoodinate:   
                        if angle < 90 and stage =='Up':
                            stage="down"
                            print(counter)
                            counter +=1
                            # print(counter)
                            print("elbow    :",y_ecoodinate)
                            print("shoulder :",y_scoodinate)
                            print(stage)  
                except:
                    pass
        
                # Render curl counter
                # Setup status box
                cv2.rectangle(image, (0,0), (225,73), (245,117,16), -1)
        
                # Rep data
                cv2.putText(image, 'REPS', (15,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                cv2.putText(image, str( counter), 
                        (10,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
                # Stage data
                cv2.putText(image, 'STAGE', (65,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                cv2.putText(image, stage, 
                        (60,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)




        

        ret,jpeg=cv2.imencode('.jpg',image)
        return jpeg.tobytes()