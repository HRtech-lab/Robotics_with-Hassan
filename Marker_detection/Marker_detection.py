
# ## Task: Detecting Markers using Vision Feedback 

# **Import packages/libraries** 

# In[1]:


import cv2
import robomaster
from robomaster import robot
from robomaster import vision


# **Create a callback function which includes a for loop based on length of marker info**
# **Market info will provide 5 values x,y, width, height and detected marker info**
# **Pass this value to MarkerInfo class**




markers = []
def on_detect_marker(marker_info):
    ##code here##
    print(marker_info)
    # x, y, width, height, detected_marker = marker_info
    # print(f"x = {x}")
    # print(f"y = {y}")
    # print(f"width = {width}")
    # print(f"height = {height}")
    # print(f"detected marker = {detected_marker}")


# **Markerinfo class will use the callback results to calulcate two points of detected object bounding box and center. The last element includes the info of the detected object**

# In[3]:


class MarkerInfo:

    def __init__(self, x, y, w, h, info):
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._info = info

    @property
    def pt1(self):
        return int((self._x - self._w / 2) * 1280), int((self._y - self._h / 2) * 720)

    @property
    def pt2(self):
        return int((self._x + self._w / 2) * 1280), int((self._y + self._h / 2) * 720)

    @property
    def center(self):
        return int(self._x * 1280), int(self._y * 720)

    @property
    def text(self):
        return self._info


# **Write the main function here**


if __name__ == '__main__':
    
    #initlize the robot
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")

    # create camera and vision object
    ep_vision = ep_robot.vision
    ep_camera = ep_robot.camera

    #start display
    ep_camera.start_video_stream(display=False)

    #callback for marker detection
    result = ep_vision.sub_detect_info(name="marker", callback=on_detect_marker)

    for i in range(0, 500):


      #read robot camera's image using cv2 

        img = ep_camera.read_cv2_image(strategy="newest", timeout=0.5)

        # create a for loop based on length on markers
        # first check what does the detected results show 
        # The callback class the marker variable with 4 elements, pt1,pt2, text, center
        # use cv2.rectangle to create bouding box for pt1 and pt2
        # use cv2.put text for text and center 
        
        ##code here##
        
        for j in range(0, len(markers)):
            cv2.rectangle(img, markers[j].pt1, markers[j].pt2, (255, 255, 255))
            cv2.putText(img, markers[j].text, markers[j].center, cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

        cv2.imshow("Markers", img)
        cv2.waitKey(1)
    cv2.destroyAllWindows()

    result = ep_vision.unsub_detect_info(name="marker")
    cv2.destroyAllWindows()
    ep_camera.stop_video_stream()
    ep_robot.close()
