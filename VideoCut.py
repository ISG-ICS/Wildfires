import cv2
# cut a 30 fps video in every second
def is_Fire(video_path):
    gap = 30
    vidcap = cv2.VideoCapture(video_path)
    success,image = vidcap.read()
    count = 0
    while success:
        if count % 30 == gap:
            cv2.imwrite("frame%d.jpg" % (count/30), image)
            print("Image ", count/30 ," printed.")
            # TODO: score = pic recognize score
        count += 1
        success,image = vidcap.read()
        # TODO : if score > 0.8: return True
        # TODO : if score > 0.5: gap = int(gap/2)  else: gap = gap * 2

    return False
is_Fire('test.mp4')
