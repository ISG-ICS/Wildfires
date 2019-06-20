import cv2

vidcap = cv2.VideoCapture('test.mp4')
success,image = vidcap.read()
count = 0

#cut a 30 fps video in every second
while success:
  if count % 30 == 0:
      cv2.imwrite("frame%d.jpg" % (count/30), image)
      print("Image ", count/30 ," printed.")
  count += 1
  success,image = vidcap.read()
  
  
  
