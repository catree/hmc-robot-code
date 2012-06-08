#!/usr/bin/env python
import roslib; roslib.load_manifest('Frizzle')
import rospy
import cv_bridge
import cv
import sensor_msgs.msg as sm

# Dictionary to hold all globals in
D = {}

####################### CALLBACK FUNCTIONS #########################
def onMouse(event, x, y, flags, param):
    """ the method called when the mouse is clicked """

    if event==cv.CV_EVENT_LBUTTONDOWN: # clicked the left button
        print "x, y are", x, y
        (b,g,r) = D["image"][y,x]
        print "r,g,b is", int(r), int(g), int(b)
        (h,s,v) = D["hsv"][y,x]
        print "h,s,v is", int(h), int(s), int(v)


def check_key_press(key_press):
    """ this handler is called when a real key press has been
        detected, and updates everything appropriately
    """
    global D
    D["last_key_pressed"] = key_press

    if key_press == ord('q') or key_press == 27: # if a 'q' or ESC was pressed
        print "quitting"
        rospy.signal_shutdown( "Quit requested from keyboard" )
    elif key_press == ord('h'):
        print " Keyboard Command Menu"
        print " =============================="
        print " q    : quit"
        print " ESC  : quit"
        print " h    : help menu"
        print " t    : show total threshold image in threshold window"
        print " r    : show red image in threshold window"
        print " g    : show green image in threshold window"
        print " b    : show blue image in threshold window"
        print " y    : show thresholded red image in threshold window"
        print " u    : show thresholded blue image in threshold window"
        print " i    : show thresholded green image in threshold window"
        print " a    : show hue image in threshold window"
        print " s    : show saturation image in threshold window"
        print " d    : show value image in threshold window"
        print " z    : show thresholded hue image in threshold window"
        print " x    : show thresholded saturation image in threshold window"
        print " c    : show thresholded value image in threshold window"
    elif key_press == ord('t'):
        D["current_threshold"] = "threshed_image"
    elif key_press == ord('r'):
        D["current_threshold"] = "red"
    elif key_press == ord('g'):
        D["current_threshold"] = "green"
    elif key_press == ord('b'):
        D["current_threshold"] = "blue"
    elif key_press == ord('y'):
        D["current_threshold"] = "red_threshed"
    elif key_press == ord('u'):
        D["current_threshold"] = "green_threshed"
    elif key_press == ord('i'):
        D["current_threshold"] = "blue_threshed"
    elif key_press == ord('a'):
        D["current_threshold"] = "hue"
    elif key_press == ord('s'):
        D["current_threshold"] = "sat"
    elif key_press == ord('d'):
        D["current_threshold"] = "val"
    elif key_press == ord('z'):
        D["current_threshold"] = "hue_threshed"
    elif key_press == ord('x'):
        D["current_threshold"] = "sat_threshed"
    elif key_press == ord('c'):
        D["current_threshold"] = "val_threshed"

# Functions for changing the slider values
def change_low_red(new_threshold):
    global D
    D["low_red"] = new_threshold

def change_high_red(new_threshold):
    global D
    D["high_red"] = new_threshold

def change_low_green(new_threshold):
    global D
    D["low_green"] = new_threshold

def change_high_green(new_threshold):
    global D
    D["high_green"] = new_threshold

def change_low_blue(new_threshold):
    global D
    D["low_blue"] = new_threshold

def change_high_blue(new_threshold):
    global D
    D["high_blue"] = new_threshold

def change_low_hue(new_threshold):
    global D
    D["low_hue"] = new_threshold

def change_high_hue(new_threshold):
    global D
    D["high_hue"] = new_threshold

def change_low_sat(new_threshold):
    global D
    D["low_sat"] = new_threshold

def change_high_sat(new_threshold):
    global D
    D["high_sat"] = new_threshold

def change_low_val(new_threshold):
    global D
    D["low_val"] = new_threshold

def change_high_val(new_threshold):
    global D
    D["high_val"] = new_threshold


##################### END CALLBACK FUNCTIONS #######################

#################### INITIALIZATION FUNCTIONS ######################
def init_globals():
    """ sets up all the globals in the dictionary D
    """
    # get D so that we can change values in it
    global D

    # put threshold values into D
    D['low_red'] = 0
    D['high_red'] = 255
    D['low_green'] = 0
    D['high_green'] = 255
    D['low_blue'] = 0
    D['high_blue'] = 255
    D['low_hue'] = 0
    D['high_hue'] = 255
    D['low_sat'] = 0
    D['high_sat'] = 255
    D['low_val'] = 0
    D['high_val'] = 255

    # Set up the windows containing the image from the kinect,
    # the altered image, and the threshold sliders.
    cv.NamedWindow('image')
    cv.MoveWindow('image', 0, 0)
    cv.NamedWindow('threshold')
    cv.MoveWindow('threshold', 640, 0)
    cv.NamedWindow('sliders')
    cv.MoveWindow('sliders', 1280, 0)

    # Create the sliders within the 'sliders' window
    cv.CreateTrackbar('low_red', 'sliders', D['low_red'], 255, change_low_red)
    cv.CreateTrackbar('high_red', 'sliders', D['high_red'], 255, change_high_red)
    cv.CreateTrackbar('low_green', 'sliders', D['low_green'], 255, change_low_green)
    cv.CreateTrackbar('high_green', 'sliders', D['high_green'], 255, change_high_green)
    cv.CreateTrackbar('low_blue', 'sliders', D['low_blue'], 255, change_low_blue)
    cv.CreateTrackbar('high_blue', 'sliders', D['high_blue'], 255, change_high_blue)
    cv.CreateTrackbar('low_hue', 'sliders', D['low_hue'], 255, change_low_hue)
    cv.CreateTrackbar('high_hue', 'sliders', D['high_hue'], 255, change_high_hue)
    cv.CreateTrackbar('low_sat', 'sliders', D['low_sat'], 255, change_low_sat)
    cv.CreateTrackbar('high_sat', 'sliders', D['high_sat'], 255, change_high_sat)
    cv.CreateTrackbar('low_val', 'sliders', D['low_val'], 255, change_low_val)
    cv.CreateTrackbar('high_val', 'sliders', D['high_val'], 255, change_high_val)

    # Set the method to handle mouse button presses
    cv.SetMouseCallback('image', onMouse, None)

    # We have not created our "scratchwork" images yet
    D["created_images"] = False

    # Variable for key presses
    D["last_key_pressed"] = 255

    # The current image we want to display in the threshold window
    D["current_threshold"] = "threshed_image"

    # Create a connection to the Kinect
    D["bridge"] = cv_bridge.CvBridge()


def init_images():
    """ Creates all the images we'll need. Is separate from init_globals 
        since we need to know what size the images are before we can make
        them
    """
    global D

    # Find the size of the image 
    # (we set D["image"] right before calling this function)
    D["size"] = cv.GetSize(D["image"])

    # Create images for each color channel
    D["red"] = cv.CreateImage(D["size"], 8, 1)
    D["blue"] = cv.CreateImage(D["size"], 8, 1)
    D["green"] = cv.CreateImage(D["size"], 8, 1)
    D["hue"] = cv.CreateImage(D["size"], 8, 1)
    D["sat"] = cv.CreateImage(D["size"], 8, 1)
    D["val"] = cv.CreateImage(D["size"], 8, 1)

    # Create images to save the thresholded images to
    D["red_threshed"] = cv.CreateImage(D["size"], 8, 1)
    D["green_threshed"] = cv.CreateImage(D["size"], 8, 1)
    D["blue_threshed"] = cv.CreateImage(D["size"], 8, 1)
    D["hue_threshed"] = cv.CreateImage(D["size"], 8, 1)
    D["sat_threshed"] = cv.CreateImage(D["size"], 8, 1)
    D["val_threshed"] = cv.CreateImage(D["size"], 8, 1)

    # The final thresholded result
    D["threshed_image"] = cv.CreateImage(D["size"], 8, 1)

    # Create the hsv image
    D["hsv"] = cv.CreateImage(D["size"], 8, 3)

################## END INITIALIZATION FUNCTIONS ####################

################### IMAGE PROCESSING FUNCTIONS #####################
def threshold_image():
    """ runs the image processing in order to create a 
        black and white thresholded image out of D["image"]
        into D["threshed_image"]
    """
    global D

    # Use OpenCV to split the image up into channels,
    # saving them in their respective bw images
    cv.Split(D["image"], D["blue"], D["green"], D["red"], None)

    # This line creates a hue-saturation-value image
    cv.CvtColor(D["image"], D["hsv"], cv.CV_RGB2HSV)
    cv.Split(D["hsv"], D["hue"], D["sat"], D["val"], None)

    # Here is how OpenCV thresholds the images based on the slider values:
    cv.InRangeS(D["red"], D["low_red"], D["high_red"], D["red_threshed"])
    cv.InRangeS(D["blue"], D["low_blue"], D["high_blue"], D["blue_threshed"])
    cv.InRangeS(D["green"], D["low_green"], D["high_green"], D["green_threshed"])
    cv.InRangeS(D["hue"], D["low_hue"], D["high_hue"], D["hue_threshed"])
    cv.InRangeS(D["sat"], D["low_sat"], D["high_sat"], D["sat_threshed"])
    cv.InRangeS(D["val"], D["low_val"], D["high_val"], D["val_threshed"])

    # Multiply all the thresholded images into one "output" image,
    # named D["threshed_image"]
    cv.Mul(D["red_threshed"], D["green_threshed"], D["threshed_image"])
    cv.Mul(D["threshed_image"], D["blue_threshed"], D["threshed_image"])
    cv.Mul(D["threshed_image"], D["hue_threshed"], D["threshed_image"])
    cv.Mul(D["threshed_image"], D["sat_threshed"], D["threshed_image"])
    cv.Mul(D["threshed_image"], D["val_threshed"], D["threshed_image"])

    # Erode and Dilate shave off and add edge pixels respectively
    cv.Erode(D["threshed_image"], D["threshed_image"], iterations = 1)
    cv.Dilate(D["threshed_image"], D["threshed_image"], iterations = 1)


def find_biggest_region():
    """ finds all the contours in threshed image, finds the largest of those,
        and then marks in in the main image
    """
    global D

    # Create a copy image of thresholds then find contours on that image
    storage = cv.CreateMemStorage(0) # Create memory storage for contours
    copy = cv.CreateImage(D["size"], 8, 1)
    cv.Copy( D["threshed_image"], copy ) # copy threshed image

    # this is OpenCV's call to find all of the contours:
    contours = cv.FindContours(copy, storage, cv.CV_RETR_EXTERNAL, \
                                   cv.CV_CHAIN_APPROX_SIMPLE)

    # Next we want to find the *largest* contour
    if len(contours) > 0:
        biggest = contours
        biggestArea = cv.ContourArea(contours)
        while contours != None:
            nextArea = cv.ContourArea(contours)
            if biggestArea < nextArea:
                biggest = contours
                biggestArea = nextArea
            contours = contours.h_next()
        
        # Use OpenCV to get a bounding rectangle for the largest contour
        br = cv.BoundingRect(biggest, update=0)
        
        # Draw a box around the largest contour, and a circle at its center
        cv.PolyLine(D["image"], [[(br[0], br[1]), (br[0], br[1] + br[3]), \
                                      (br[0] + br[2], br[1] + br[3]), \
                                      (br[0] + br[2], br[1])]],\
                        1, cv.RGB(255, 0, 0))

        # Draw the circle:
        cv.Circle(D["image"], (br[0] + int(br[2]/2), br[1] + int(br[3]/2)), 10, \
                      cv.RGB(255, 255, 0), thickness=1, lineType=8, shift=0)

        # Draw the contours in white with inner ones in green
        cv.DrawContours(D["image"], biggest, cv.RGB(255, 255, 255), \
                            cv.RGB(0, 255, 0), 1, thickness=2, lineType=8, \
                            offset=(0,0))

################# END IMAGE PROCESSING FUNCTIONS ###################

def handle_data(data):
    """ this method processes data given:
        - key presses
        - images from Kinect
    """
    global D
    # Get the incoming image from the Kinect
    D["image"] = D["bridge"].imgmsg_to_cv(data, "bgr8")

    if D["created_images"] == False:
        # Initialize the additional images we need for processing
        # We only need to run this one time
        init_images()
        D["created_images"] = True

    # Recalculate threshold image
    threshold_image()

    # Recalculate blob in main image
    find_biggest_region()

    # Get any incoming keypresses
    # To get input from keyboard, we use cv.WaitKey
    # Only the lowest eight bits matter (so we get rid of the rest):
    key_press_raw = cv.WaitKey(5) # gets a raw key press
    key_press = key_press_raw & 255 # sets all but the low 8 bits to 0
    
    # Handle key presses only if it's a real key (255 = "no key pressed")
    if key_press != 255:
        check_key_press(key_press)

    # Update the displays:
    # Main image:
    cv.ShowImage('image', D["image"])

    # Currently selected threshold image:
    cv.ShowImage('threshold', D[ D["current_threshold"] ] )

def main():
    """ the main program that sets everything up and initializes everything
    """
    
    # Initialize our node
    rospy.init_node('blobFinder')

    # Initialize all the global variables we will need
    init_globals()

    # Subscribe to the image_color topic
    # Each time new data comes in (Kinect color image, keypresses), we will call handle_data 
    # to deal with it
    rospy.Subscriber('/camera/rgb/image_color', sm.Image, handle_data)

    # Run until something stops us, such as a call to rospy.signal_shutdown
    rospy.spin()

# this is the "main" trick: it tells Python
# what code to run when you run this as a stand-alone script:
if __name__ == "__main__":
    main()
