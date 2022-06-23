# ## Task: Boundary Following using IR Sensors 

# **Import packages/libraries** </br>

import robomaster

import time

from robomaster import robot


# **You can Initialize variables in this block** </br>

# In[2]:


slp = 0.2

left_distance = 0 


# **Define the callback function to get robot's IR sensor data**
# 
# **You should assign values to global variables so we can use them in the main function**
# 
# **Make sure you check on which index of sub_info are you getting left sensor value readings** 

# In[3]:


def sub_data_handler(sub_info):
    
    ##code here##
    global left_distance
    left_distance = sub_info[2]


# **Similar to as done previously for teleop code, define the various movements of robot motion by controlling wheel velocity** 

# In[4]:


def forward(vel):
    
    #use the drive_wheels function to move the robot forward 
    
    ##code here##
    ep_chassis.drive_wheels(w1 = vel, w2 = vel, w3 = vel, w4 = vel)
    time.sleep(slp)

    kill()


# In[5]:


def sharp_right(vel):
    
    ##code here##
    ep_chassis.drive_wheels(w1 = -vel, w2 = vel, w3 = 0,w4 = 0)
    time.sleep(slp)
    
    kill()


# In[6]:


def forward_right(vel):

    ##code here##
    ep_chassis.drive_wheels(w1 = -vel, w2 = vel, w3 = vel, w4 = vel)
    time.sleep(slp)
    kill()


# In[7]:


def forward_left(vel): 
    ##code here##
    ep_chassis.drive_wheels(w1 = vel, w2 = -vel, w3 = vel, w4 = vel)
    time.sleep(slp)
    kill()


# In[8]:


def kill():

    ep_chassis.drive_wheels(w1 = 0, w2 = 0, w3 = 0, w4 = 0)


# **Write the Main Function here**

# In[9]:


if __name__ == '__main__':


    ep_robot = robot.Robot()
    
    ep_robot.initialize(conn_type="ap")                                 #Initialize the connection type - ap is for wifi connection 
    
    ep_chassis = ep_robot.chassis                                       #Initialize the chassis 
    
    ep_sensor = ep_robot.sensor                                         #Initialize the IR_sensor 
    
    ep_sensor_adaptor = ep_robot.sensor_adaptor                         #Initialize the sensor adapter 
    
    ep_sensor.sub_distance(freq=10, callback=sub_data_handler)          #Get current IR sensor data using the callback function 
    
    
    while(1):
#         forward(30)
        front_distance = ep_sensor_adaptor.get_adc(id=1, port=1) #Get current sharp sensor data using the get_adc function of SensorAdapter
        
        print("left_distance:{0}, front_distance{1}".format(left_distance, front_distance))
        
    
        ###########################################################################
        
        #Use the left_sensor, and front_sensor data to move the robot such that it:
            ##adjusts itself if it is too far from the wall
            ##adjusts itself it it is too close to the wall
            ##takes a sharp turn if it encounters an obstacle
        
        ##code here##
        vel = 60
        if left_distance < 80:
            forward_right(vel)
        if front_distance > 350:
            sharp_right(vel)
        else:
            forward(vel)
        
        ##########################################################################
        

    ep_robot.close()
