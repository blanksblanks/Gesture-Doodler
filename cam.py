import cv2, time, sys, os
import numpy as np

# Camera 0 is the integrated web cam
camera_port = 0
frame_size = 640
timer = 5
file_count = 1
dir_name = "live_captures/"+str(int(time.time()))

# Initialize the camera capture object with the cv2.VideoCapture class.
# All it needs is the index to a camera port.
camera = cv2.VideoCapture(camera_port)
camera.set(3, frame_size)
camera.set(4, frame_size)

def draw_quadrants(size, frame):
    h1 = int(size/3)
    h2 = size - int(size/3)
    v1 = int(size/3)
    v2 = size - int(size/3)
    lst = [(0,h1), (size,h1), (0,h2), (size,h2), (v1,0), (v1,size), (v2,0), (v2,size)]
    for i in xrange(0, len(lst), 2):
        a = lst[i]
        b = lst[i+1]
        cv2.line(frame,a,b,[128,128,128],1)

# Captures a single image from the camera and returns it in PIL format
def get_image():
    # read is the easiest way to get a full image out of a VideoCapture object.
    retval, im = camera.read()
    return im

def write_file_to_disk():
    global file_count
    global camera
    global dir_name
    # take the actual image we want to keep
    print('\nCapturing image!')
    camera_capture = get_image()
    imageFile = "./" + dir_name + "/file_"+ str(file_count) + ".JPG"
    print 'Writing image file to', imageFile, '\n'
    # nice feature of the imwrite method is that it will automatically choose the
    # correct format based on the file extension you provide. Convenient!
    cv2.imwrite(imageFile, camera_capture)
    file_count += 1

    if file_count > 3:
        camera.release()
        # read the fresh sequence of gestures
        ''' TODO: link these classes properly instead of hijacking os system '''
        os.system("python vislock.py " + dir_name)
    else:
        open_camera_feed()

def open_camera_feed():
    global camera
    global dir_name
    global frame_size

    # create directory
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    local_timer = timer
    start_time = int(time.time());

    while (camera.isOpened and local_timer <= timer):
        val, frame = camera.read() # read the frame
        draw_quadrants(frame_size, frame)
        cv2.imshow('video', frame)

        reverse_timer = timer - local_timer
        mins, secs = divmod(reverse_timer, 60)
        timeformat ='\rTaking image in... {:02d}:{:02d} seconds'.format(mins, secs)
        sys.stdout.write(timeformat)
        sys.stdout.flush()
        local_timer = int(time.time()) - start_time
    write_file_to_disk()


if __name__ == "__main__":
    open_camera_feed()

