# import cv2
from ultralytics import YOLO
import numpy as np
from datetime import datetime

# video_file1 = "KNJ1873\KNJ1873 - Front.mp4"
# video_file2 = "KNJ1873\KNJ1873 - R.mp4" 
# video_file3="KNJ1873\KNJ1873-M.mp4"

# video1 = cv2.VideoCapture(video_file1)
# video2 = cv2.VideoCapture(video_file2)
# video3 = cv2.VideoCapture(video_file3)
# ret, frame1 = video1.read()
# ret, frame2 = video2.read()
# ret, frame3 = video3.read()
def count(frame1,frame2,frame3, model):
 # Read the video frames
    # re_width = int(int(video1.get(cv2.CAP_PROP_FRAME_WIDTH))*0.5)
    # re_height = int(int(video1.get(cv2.CAP_PROP_FRAME_HEIGHT))*0.5)

    # Track objects in frames if available
    results1 = model(frame1,conf=0.3, iou=0.9,classes=0,show=False,verbose=False)
    results2 = model(frame2,conf=0.3, iou=0.9,classes=0,show=False,verbose=False)
    results3 = model(frame3,conf=0.3, iou=0.9,classes=0,show=False,verbose=False)
    count=0
    for result in [results1,results2,results3]:
        for res in result:
            arrxy=res.boxes.xyxy
            coordinates = np.array(arrxy)
            count=len(coordinates)
            count+=count
    # print("number of persons counted....",count)
    # minute = now.strftime("%M")
    # sec = now.strftime("%S")
    date_now = datetime.now().strftime("%d/%m/%Y")
    time_now = datetime.now().strftime("%H:%M:%S")
    return {"Date ":str(date_now),"Time ":str(time_now),"Bus number ":"KNJ1873 ","People count": int(count),"Latitude point":"13.082680","Longitude point":"80.270721","Bus id":"32r23e32e","Camera id" :"43r34e33434"}


    # res_plotted1 = results1[0].plot()
    # res_plotted2= results2[0].plot()
    # res_plotted3 = results3[0].plot()
    # res_plotted1 = cv2.resize(res_plotted1,(re_width,re_height))
    # res_plotted2= cv2.resize(res_plotted2,(re_width,re_height))
    # res_plotted3 = cv2.resize(res_plotted3,(re_width,re_height))
    # cv2.imshow(f"Tracking_Stream_{1}", res_plotted1)
    # cv2.imshow(f"Tracking_Stream_{2}", res_plotted2)
    # cv2.imshow(f"Tracking_Stream_{3}", res_plotted3)



# video1.release()
# video2.release()
# video3.release()

# model = YOLO('yolov8x.pt')
model = YOLO('yolov8x-seg.pt')



if __name__=="__main__":
    # count(video_file1,video_file2,video_file3, model)
    pass