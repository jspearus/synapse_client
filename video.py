import cv2
from multiprocessing import Process

videoIsPlaying = False



def start_video_loop():
    global videoIsPlaying
    videoIsPlaying = True
    video_file_name = '/home/jeff/Videos/snow2.mp4'  # Replace with your video path
    window_name = 'Repeating Video'
    while videoIsPlaying:
        video = cv2.VideoCapture(video_file_name)
        
        # Optional: set window to full screen
        cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        
        while video.isOpened():
            ret, frame = video.read()
            if ret:
                cv2.imshow(window_name, frame)
                # Press 'ESC' (key code 27) to exit the loop
                if cv2.waitKey(25) & 0xFF == 27:
                    video.release()
                    cv2.destroyAllWindows()
                    return
            else:
                # Reached the end of the video, restart the loop
                break
                
        video.release()


def stop_video_loop():
    global videoIsPlaying
    videoIsPlaying = False
    cv2.destroyAllWindows()

def runVideoOn():
    pProc = Process(target=start_video_loop, args=())
    pProc.start()   

def runVideoOff():
    poProc = Process(target=stop_video_loop, args=())
    poProc.start()  