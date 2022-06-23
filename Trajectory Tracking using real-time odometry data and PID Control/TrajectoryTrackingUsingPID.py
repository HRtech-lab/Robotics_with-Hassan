
#Trajectory Tracking using real-time odometry data and PID Control 

# **Import packages/libraries** </br>

import robomaster

import math

from robomaster import robot

import time


# **You can Initialize variables in this block** </br>

current_x = 0

current_y = 0

yaw = 0

theta_des = 0

#Initialize Kp, Ki and Kd variables 
Kp = 0.5
Ki = 0.00001
Kd = 1


# **Define the callback function to get robot's current position** </br>
# 
# **You should assign values to global variables so we can use them in the main function** </br>

# In[3]:


def sub_position_handler(position_info):
    
    global current_x
    
    global current_y

    current_x = position_info[0]
    current_y = position_info[1]
    
    # print(position_info)
    ##code here##


# **Define the callback function to get robot current position** </br>

# In[4]:


def sub_attitude_info_handler(attitude_info):
    
    global yaw
    yaw = attitude_info[0] * math.pi/180
    # print(attitude_info)
    
    ##code here##


# **Define a function that calculates the euclidean distance between the current position and the goal position** </br>
# 
# **Distance : d = √[(x2 – x1)^2 + (y2 – y1)^2]** </br>
# 

# In[5]:


def distance(goal_x, goal_y, current_x, current_y):
    
    ##code here##
    dist = math.sqrt(math.pow(goal_x - current_x, 2) + math.pow(goal_y - current_y, 2))
    return dist


# **Define a function that calculates the desired angle**
# 
# **Use the following formula to convert gradient of line to theta:
# Theta=atan(gradient)**
# 
# **Make sure you convert theta into degrees**
# 

# In[6]:


def desired_theta(goal_x, goal_y, current_x, current_y):
    
    global theta_des
    
    ##code here##
    theta_des = math.atan((goal_y - current_y)/ (goal_x - current_x))
    


# **Write the Main Function here**
# 
# **Implement PID control**
# ![image.png](data:image/png;base64,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)

# In[8]:


if __name__ == '__main__':

    slp = 0.2
    
    ep_robot = robot.Robot()                                                    #Initialize the robot
    
    ep_robot.initialize(conn_type="ap")                                         #Initialize connection type - ap is for wifi connection 

    ep_chassis = ep_robot.chassis                                               #Initialize chassis
    
    ep_chassis.sub_position(freq=10, callback=sub_position_handler)             #Get current position data using the position callback function
    
    ep_chassis.sub_attitude(freq=10, callback=sub_attitude_info_handler)        #Get current orientation data using the orientation callback function

    #Take Goal position as input from the user
    
    goal_x = int(input("enter x coordinate of goal position = "))
    
    goal_y = int(input("enter y coordinate of goal position = "))
    
    #Call the distance function to generate the first control input
    
    ##Code Here##

    distance_error = distance(goal_x, goal_y, current_x, current_y)

    angle_errs = []
    dist_errs = []

    
    #Hint: For PID you can use a loop with some error threshold as the exit condition
    while (distance_error >= 0.3):


    #Call the theta function for the required angle.
    ##Code here##
        desired_theta(goal_x, goal_y, current_x, current_y)
    
    

    #Use these errors to control your robots movements
    #Use Yaw from the robots orientation to calculate the error in angle
        error =  yaw - theta_des

    #Implement PID control. Start by only Proportional, then work your way to integral and the derivative. Kp,ki and kd are error constants.
    ##Code Here##
        angle_errs.append(error)
        dist_errs.append(distance_error)

        angle_error = Kp*error + Ki * sum(angle_errs)
        dist_errs_sum = sum(dist_errs)
        u_dist = 1*distance_error + 0.2* dist_errs_sum
        angle_error = math.atan2(math.sin(angle_error), math.cos(angle_error))

        angle_error = angle_error * 180 / math.pi

    
    
    
    
    #The robot doesnt rotate below 15 so we set a threshold of 15
        angle_speed=max([15,angle_error])
        
    #Create condition for when the angle_error is positive and negative
        if angle_error < 0:
            
            angle_speed = -angle_speed
            
        if angle_error >= 0:
            
            angle_speed = angle_speed

    #Call the distance function to get the distance error
        distance_error = distance(goal_x, goal_y, current_x, current_y)
        
    #Create threshholds for the rotation and linear movement towards goal 
        print("angle err:", angle_error)
        print(u_dist)
        if abs(angle_error) >= 5:
            
          #Incorporate the angular_speed in the robot drive_wheels function
            v = angle_speed 
            ep_chassis.drive_wheels(w1=v, w2=-v, w3=0, w4=0)
            time.sleep(slp)
            ep_chassis.drive_wheels(w1 = 0, w2 = 0, w3 = 0, w4 = 0)
            
          ##Code here##
            
        elif abs(angle_error) < 5 and u_dist >= 0.8:
            
            #Now angular error is low so incorporate the linear_speed in the robot drive_wheels function
            
            #distance_error should be multiplied by some constant to find linear speed
            
            ##Code here##
            v = u_dist * 6
            ep_chassis.drive_wheels(w1=v, w2=v, w3=v, w4=v)
            time.sleep(slp)
            ep_chassis.drive_wheels(w1 = 0, w2 = 0, w3 = 0, w4 = 0)
            
            
        else:
            ep_chassis.drive_wheels(w1 = 0, w2 = 0, w3 = 0, w4 = 0)
            
          #this condition is for when we have reached the goal
            break
          ##Code here##

            
    ep_chassis.unsub_position()
    
    ep_chassis.unsub_attitude()
    
    ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)
    
    ep_robot.close()
