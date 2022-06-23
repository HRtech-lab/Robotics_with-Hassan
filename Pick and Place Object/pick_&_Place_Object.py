# Task: Pick and Place Object 
# **Import packages/libraries.** </br>
import cv2
import robomaster
import time
import math 
from robomaster import robot
from robomaster import vision


# **These are the two classes for Marker and point. (You have seen these before)**

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

class PointInfo:

    def __init__(self, x1, y1, theta, c):
        self._x = x1
        self._y = y1
        self._theta = theta
        self._c = c

    @property
    def pt(self):
        return int(self._x1 * 1280), int(self._y1 * 720)

    @property
    def color(self):
        return 255, 255, 255


# **You can Initialize variables in this block**

# In[3]:


line = []        
markers = []
slp = 0.2
x_marker = 0
y_marker = 0
x_line = 0
y_line = 0 
number = 0 
sensor_distance = 0


# **Define the callback function to get sensor information.**
# 
# **You should assign values to global variables so we can use them in the main function.**

# In[4]:


def sub_data_handler(sub_info):
    global sensor_distance
    ##Code here##
    sensor_distance = sub_info[2]  #Sensor Info


# **Define the callback function to detect Marker.**

# In[5]:


def on_detect_marker(marker_info):
    global x_marker
    global y_marker 
    global number
    number = len(marker_info)
    markers.clear()

    
    for i in range(0, number):
        x, y, w, h, info = marker_info[i]
        markers.append(MarkerInfo(x, y, w, h, info))
        x_marker = x
        y_marker = y  
        print("marker:{0} x:{1}, y:{2}, w:{3}, h:{4}".format(info, x, y, w, h))
        


# **Define the callback function to detect Line.**

# In[6]:


def on_detect_line(line_info):
    global x_line 
    global y_line
    number1 = len(line_info)
    print(line_info)
    print("number")
    print(number1)
    line.clear()
    line_type = line_info[0]
    print('line_type', line_type)
    for i in range(1, number1):
        x1, y1, ceta, c = line_info[i]
        x_line = x1
        y_line = y1
        line.append(PointInfo(x1, y1, ceta, c))
        print("x{0}, y{1}, ceta{2}, c{3}".format(x1,y1,ceta,c))


# **Define a function that moves the gripper to grab the bottle.**
# 

# In[22]:


def gripper_movement():
    ep_gripper.open(power=35)
    time.sleep(1)
    ##Code here##
    ep_arm.move(x=100, y=20).wait_for_completed() #Moving the arm
    time.sleep(1)
    ep_gripper.close(power=45)
    time.sleep(1)
    ep_gripper.pause()
    ep_arm.move(x=-50, y=0).wait_for_completed() #Moving the arm
    time.sleep(1)
    ep_arm.move(x=0, y=-10).wait_for_completed() #Moving the arm
    time.sleep(1)


# In[8]:


# def gripper_open():
#     ep_gripper.open(power=50)
#     time.sleep(1)
#     ep_gripper.pause()


# **Define a function that detects the marker and corrects its position. (Moves Left or Right)**
# 
# **Hint: You can create an infinite loop with an error threshold as its exit condition**

# In[9]:


def marker_detection1():
    ep_vision.sub_detect_info(name="marker", callback=on_detect_marker)
    ##Code here##
#     print(result)
#Define initial error
    error = 0.5 - x_marker
    print("marker has been detected")
    while(abs(error) > 0.015):
        ep_vision.sub_detect_info(name="marker", callback=on_detect_marker)
        print("xmarker = ",x_marker)
    	##Code here##
#         print(result)
	#Define error again in the loop 
        error = 0.5 - x_marker
        if error < 0: #move right
    		##Code here##
            ep_chassis.drive_wheels(w1 = -vel, w2 = vel, w3 = -vel, w4 = vel)
            time.sleep(slp)
            # kill()
        elif error > 0: #move left 
    		##Code here##
            ep_chassis.drive_wheels(w1 = vel, w2 = -vel, w3 = vel, w4 = -vel)
            time.sleep(slp)
            # kill()
        else:
    		##Code here##
            kill()
    kill()
#             time.sleep(slp)


# **Define a function that corrects the robots heading with respect to marker. (It rotates to find the marker)**

# In[30]:


def marker_detection_heading():
    ep_vision.sub_detect_info(name="marker", callback=on_detect_marker)
    while(number == 0): #rotate until a marker 2 comes in field of view of robot 
        ##Code here##
        #Rotate the robot
        ep_chassis.move(x=0,y=0,z=-25,xy_speed=0.7).wait_for_completed()
        
#         error = 0.5 - x_marker
        if x_marker > 0 and x_marker < 0.45: #move right
            theta = -45-(87*x_marker)
            ep_chassis.move(x=0,y=0,z=theta,xy_speed=0.7).wait_for_completed()
            kill()
            time.sleep(slp)
        if x_marker > 0.55 and x_marker < 1: 
            theta = 45-(87*x_marker)
            ep_chassis.move(x=0,y=0,z=theta,xy_speed=0.7).wait_for_completed()
            kill()
            time.sleep(slp)
        else:
            kill()
        kill()


# In[11]:


def marker_detection2():
    ep_vision.sub_detect_info(name="marker", callback=on_detect_marker)
    while(number == 0): #rotate until a marker 2 comes in field of view of robot 
        ##Code here##
        #Rotate the robot
        ep_chassis.move(x=0,y=0,z=-5,xy_speed=0.7).wait_for_completed()
    #We want the marker in the middile of the screen
    ##Code here##
        error = 0.5 - x_marker
        while(abs(error) > 0.015):
            ep_vision.sub_detect_info(name="marker", callback=on_detect_marker)
            ##Code here##
    #         print(result)
        #Define error again in the loop 
            error = 0.5 - x_marker
            if error < 0: #move right
                ##Code here##
                ep_chassis.drive_wheels(w1 = -vel, w2 = vel, w3 = -vel, w4 = vel)
                time.sleep(slp)
                # kill()
            elif error > 0: #move left 
                ##Code here##
                ep_chassis.drive_wheels(w1 = vel, w2 = -vel, w3 = vel, w4 = -vel)
                time.sleep(slp)
                # kill()
            else:
                ##Code here##
                kill()
        kill()


# **Define a function to detect line and align itself with respect to it.**

# In[ ]:


vel1 = 10
def line_detection():
    ##Code here##
    ep_vision.sub_detect_info(name="line", color="blue", callback=on_detect_line)
    #Define initial error
    error = 0.5 - x_line
    while(abs(error) > 0.03):
        ep_vision.sub_detect_info(name="line", color="blue", callback=on_detect_line)
        error = 0.5 - x_line
        if error < 0: #move right
    		##Code here##
            ep_chassis.drive_wheels(w1 = -vel1, w2 = vel1, w3 = -vel1, w4 = vel1)
            time.sleep(slp)
            # kill()
        elif error > 0: #move left 
    		##Code here##
            ep_chassis.drive_wheels(w1 = vel1, w2 = -vel1, w3 = vel1, w4 = -vel1)
            time.sleep(slp)
            # kill()
        else:
    		##Code here##
            kill()
    kill()


# **Define a function that moves the robot forward at a specific velocity.**

# In[13]:


def forward(vel):
    ##Code here##
    ep_chassis.drive_wheels(w1 = vel, w2 = vel, w3 = vel, w4 = vel)
    time.sleep(slp)
    kill()


# In[14]:


def backward(vel):
    ##Code here##
    ep_chassis.drive_wheels(w1 = -vel, w2 = -vel, w3 = -vel, w4 = -vel)
    time.sleep(slp)
    kill()


# **Define a function that stops the robot. (Velocity = 0)**

# In[15]:


def kill():
    ##Code here##
    ep_chassis.drive_wheels(w1 = 0, w2 = 0, w3 = 0, w4 = 0)


# **Write the Main Function here.**
# 
# **Implement Object Detection.**

# In[ ]:


if __name__ == '__main__':

    #Initialize Robot parameters
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")

    ep_vision = ep_robot.vision
    ep_camera = ep_robot.camera
    ep_chassis = ep_robot.chassis
    ep_sensor = ep_robot.sensor
    ep_arm = ep_robot.robotic_arm
    ep_gripper = ep_robot.gripper
    
    ep_sensor.sub_distance(freq=5, callback=sub_data_handler)
    ep_camera.start_video_stream(display=False)
     
    ##Code here##
    
    #################################################################
    #You need to use your defined functions to centre the first marker on the screen, move towards the marker until some distance threshold,
    # grab the object using gripper and move a little back to make space for the next operation,
    # locate the second marker (rotate), move towards the second marker and drop the object
    #################################################################
    vel = 30
    marker_detection1() #calling the funtion
    while sensor_distance > 220:
        forward(vel)
    kill()
    
    result = ep_vision.unsub_detect_info(name="marker")
    ep_vision.sub_detect_info(name="line", color="blue", callback=on_detect_line)
    line_detection()
   
    gripper_movement()
    backward(vel)
    
    ep_arm.move(x=0, y=-5).wait_for_completed() #Moving the arm
    time.sleep(1)
    
    ep_vision.unsub_detect_info(name="line")

    marker_detection_heading()
    marker_detection2()
    ep_arm.move(x=0, y=25).wait_for_completed() #Moving the arm
    time.sleep(1)
    while sensor_distance > 220:
        forward(vel)
    kill()
    
    
    ep_gripper.open(power=35)
    time.sleep(1)
    
    cv2.destroyAllWindows()
    ep_sensor.unsub_distance()
    cv2.destroyAllWindows()
    ep_camera.stop_video_stream()
    ep_robot.close()
