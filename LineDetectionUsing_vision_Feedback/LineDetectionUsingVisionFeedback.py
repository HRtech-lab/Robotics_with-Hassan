# **Import packages/libraries** 
import cv2
import robomaster
from robomaster import robot
from robomaster import vision


# **Create a callback for line info. Append the values in line**
# 
# **-Line_info includes 5 elements**
# 
# **-1st variable incldues info regarding line type**
# 
# **-2nd, and 3rd and x and y position**
# 
# **-4th is theta**
# 
# **-5th is center**
# 
# **-pass these values to Pointinfo class and append the final values in line array**

# In[2]:


line = []

def on_detect_line(line_info):
    number = len(line_info)
    line.clear()
    for i in range(1, number):
        x, y, ceta, c = line_info[i]
        line.append(PointInfo(x, y, ceta, c))
        print(line_info)


# **This class provides position of line and the color of line**

# In[3]:


class PointInfo:

    def __init__(self, x, y, theta, c):
        self._x = x
        self._y = y
        self._theta = theta
        self._c = c

    @property
    def pt(self):
        return int(self._x * 1280), int(self._y * 720)

    @property
    def color(self):
        return 255, 255, 255


# **Write the main function here**

# In[ ]:



if __name__ == '__main__':

    #initialize the robot
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")
    
    #vision and camera objects
    ep_vision = ep_robot.vision
    ep_camera = ep_robot.camera

    #start video stream
    ep_camera.start_video_stream(display=True)

    #create callback for on detect line
    result = ep_vision.sub_detect_info(name="line", color="blue", callback=on_detect_line)

    for i in range(0, 500):
        img = ep_camera.read_cv2_image(strategy="newest", timeout=0.5)

        #add a for loop based on length of line
        #use cv2.circle to draw line using position of line and color
        
        
        for j in range(0, len(line)):
            cv2.circle(img, line[j].pt, 3, line[j].color, -1)
            
        cv2.imshow("Line", img)
        cv2.waitKey(1)
    cv2.destroyAllWindows()
    result = ep_vision.unsub_detect_info(name="line")
    cv2.destroyAllWindows()
    ep_camera.stop_video_stream()
    ep_robot.close()
