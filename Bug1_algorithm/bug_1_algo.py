# Task: Bug1 

# **Import packages/libraries** </br>
import robomaster
import math
import numpy
from robomaster import robot
from robomaster import led
import time
import pandas

# **You can Initialize variables in this block** </br>

slp = 0.3

left_distance = 0 

left_distance1 = 0 

left_distance2 = 0 

curr_x = 0

curr_y = 0

curr_x1 = 0

curr_y1 = 0

curr_x2 = 0

curr_y2 = 0

curr_x3 = 0

curr_y3 = 0

yaw = 0

count = 0

flag = 0 

state = 0 


# **Defining callback functions to get robot's IR sensor data**
# 
# **Make sure you check on which index of sub_info are you getting left sensor value readings** 
# 
# **We require three different callback functions for the three different stages of the algorithm that require sensor data** 
# 

# In[ ]:


def sub_data_handler(sub_info):

    global left_distance

    left_distance = sub_info[1]
    
def sub_data_handler1(sub_info):

    global left_distance1
    
    left_distance1 = sub_info[1]

    
def sub_data_handler2(sub_info):

    global left_distance2
    
    left_distance2 = sub_info[1]
    
    
#Check It


# **Defining the callback functions to get robot's positon**
# 
# **We require four different callback functions for four different stages of the algorithm** 

# In[ ]:


def sub_position_handler(position_info):

    global curr_x
    
    global curr_y 
    
    curr_x, curr_y, z = position_info 
    
    
def sub_position_handler1(position_info):

    global curr_x1
    
    global curr_y1 
    
    curr_x1, curr_y1, z = position_info 


def sub_position_handler2(position_info):

    global curr_x2
    
    global curr_y2 
    
    curr_x2, curr_y2, z = position_info     
    
    
def sub_position_handler3(position_info):

    global curr_x3
    
    global curr_y3 
    
    curr_x3, curr_y3, z = position_info


# **Define the callback function to get robot's yaw**
# 
# **You should assign values to global variables so we can use them in the main function**

# In[ ]:


def sub_attitude_info_handler(attitude_info):

    global yaw
    
    ##code here##

    yaw = attitude_info[0] * math.pi/180


# **Defining the various movements of robot motion by controlling wheel velocity**

# In[ ]:


def forward(vel):

    ep_chassis.drive_wheels(w1 = vel, w2 = vel, w3 = vel, w4 = vel)
    
    time.sleep(slp)

    kill()

def forward_right(vel):

    ep_chassis.drive_wheels(w1 = -vel, w2 = vel, w3 = vel, w4 = vel)

    time.sleep(slp)

    kill()

def forward_left(vel):

    ep_chassis.drive_wheels(w1 = vel, w2 = -vel, w3 = vel, w4 = vel)

    time.sleep(slp)

    kill()

def sharp_right(vel):

    ep_chassis.drive_wheels(w1 = -vel, w2 = vel, w3 = 0, w4 = 0)

    time.sleep(slp)

    kill()

def sharp_left(vel):

    ep_chassis.drive_wheels(w1 = vel, w2 = -vel, w3 = 0, w4 = 0)

    time.sleep(slp)

    kill()


def kill():

    ep_chassis.drive_wheels(w1 = 0, w2 = 0, w3 = 0, w4 = 0)


# **Define a function that calculates the euclidean distance between the current position and the goal position**
# 
# **Distance : d = √[(x2 – x1)^2 + (y2 – y1)^2]**

# In[ ]:


def distance(des_x, des_y, curr_x, curr_y):
    
    ##code here##
    dist = math.sqrt(math.pow(des_x - curr_x, 2) + math.pow(des_y - curr_y, 2))
    return dist


# **Define a function that calculates the desired angle**
# 
# **Use the following formula to convert gradient of line to theta:
# Theta=atan(gradient)**
# 
# **Make sure you convert theta into degrees**

# In[ ]:


def desired_theta(des_x, des_y, curr_x, curr_y):
    
    ##code here##
    global theta_des
    
    theta_des = math.atan((des_y - curr_y)/ (des_x - curr_x))    
    return  theta_des


# **Use the trajectory tracking code written previously to define the pid function**
# 
# **use curr_x, curr_y variables where needed**

# In[ ]:


def pid(des_x, des_y, prev):

    dt = 0.01

    E_int = 0

    Kp = 0.5

    Ki = 0.000001

    Kd = 0.000001

    v0 = 50

    print("curr_x:", curr_x, "curr_y", curr_y)

    gradient = (des_y - (curr_y) )/(des_x - (curr_x))

    theta_des = math.atan(gradient)

    theta_des = (theta_des*180)/math.pi

    e =  yaw - theta_des

    E_int = E_int + e

    dev = (e - prev) / dt

    prev = e

    angle_error = Kp * e + Ki * E_int + Kd * dev

    distance_error = distance(des_x,des_y,(curr_x),(curr_y)) * 20

    return distance_error, angle_error , prev 


# **Use the trajectory tracking code written previously to define the pid function**
# 
# **use curr_x3, curr_y3 variables where needed**

# In[ ]:


def pid1(des_x, des_y, prev):

    dt = 0.01

    E_int = 0

    Kp = 0.5

    Ki = 0.000001

    Kd = 0.000001

    v0 = 50

    print("curr_x:", curr_x3, "curr_y", curr_y3)

    gradient = (des_y - (curr_y3) )/(des_x - (curr_x3))

    theta_des = math.atan(gradient)

    theta_des = (theta_des*180)/math.pi

    e =  yaw - theta_des

    E_int = E_int + e

    dev = (e - prev) / dt

    prev = e

    angle_error = Kp * e + Ki * E_int + Kd * dev
    
    distance_error = distance(des_x,des_y,(curr_x3),(curr_y3)) * 20

    return distance_error, angle_error , prev


# **Once the front sensor has detected an object the algorithm goes into state 1**
# 
# **Use the left sensor to follow the perimeter of the object**
# 
# **calculate the distance of each point from the desired point and append all three varaibles in an array until the robot reaches its initial location**
# 
# **Use curr_x1 and curr_y1 where required**
# 
# **Use left_distance1 where required**

# In[ ]:


def wallfollowing(hit_x, hit_y, des_x, des_y): 

    ep_sensor.sub_distance(freq = 20, callback = sub_data_handler1)

    ep_chassis.sub_position(freq = 20, callback = sub_position_handler1)

    #turn the robot 90 degrees by using move function such that the left sensor faces the objetc's wall 
    
    ##code here##
    ep_chassis.move(x=0, y=0, z=90).wait_for_completed()
    
    #move the robot a small distance by using move function 

    ##code here## 
    ep_chassis.move(x=0.1, y=0, z=0).wait_for_completed()
    

    #call the distacne function and store the initial distance of hit_x and hit_y from des_x and des_y in a variable called dist
    
    hit_x = curr_x
    hit_y = curr_y 
    
    dist = distance(des_x, des_y, curr_x, curr_y)

    
    
    ##code here##
   

    #store dist, hit_x and hit_y in distance_array 
    
    ##code here##
    distance_array = dict()
    distance_array[dist] = [hit_x, hit_y]

    while((abs(curr_x1) > 0.15) or (abs(curr_y1) > 0.15)): 

        print("curr_x:", curr_x1, "curr_y", curr_y1)

        #call the distance function and store it in a variable called dist
        
        ##code here##
        dist = distance(des_x, des_y, curr_x, curr_y)
        
        #create an array with dist, curr_x1 and _curr_y1 and append it in distance_array
        
        ##code here##
        distance_array[dist] = [curr_x1, curr_y1]
        
    kill()

    ep_sensor.unsub_distance()

    ep_chassis.unsub_position()

    print("reached initial position")
    
    #As robot has now completed traversing the obstacle and reached it's initial location state needs to be changed
    
    ##code here## 
    
    state = 2

    return state, distance_array


# **Using the distance_error and angle_error move the robot**

# In[ ]:


def movetogoal(distance_error, angle_error):

    angle_speed=max([15,angle_error])
    
    linear_speed = 50*distance_error  

    if angle_error < 0:

        angle_speed = -angle_speed

    elif angle_error >= 0:
    
        angle_speed = angle_speed
    
    if abs(angle_error) >= 5:

        ep_chassis.drive_wheels(w1=angle_speed, w2=-angle_speed, w3=0, w4=0)

    elif abs(angle_error) < 5 and distance_error >= 0.8:

        ep_chassis.drive_wheels(w1 = linear_speed, w2 = linear_speed, w3 = linear_speed, w4 = linear_speed)


# **Once the robot is in state 2 it needs to move to the point from where the goal position is the closest**
# 
# **Use curr_x2 and curr_y2 where required**
# 
# **Use left_distance2 where required**
# 

# In[ ]:


def movetomin(distance_array):

    ep_sensor.sub_distance(freq = 10, callback = sub_data_handler2)

    ep_chassis.sub_position(freq = 10, callback = sub_position_handler2)

    
    #find the minimum distance from distance array amd store it's corresponding x and y coordiantes in low_x and low_y respectively
    
    ##code here##
    
    min_dist = min(distance_array.keys())
    print(min_dist)
    min_point = distance_array[min_dist]
    low_x = min_point[0]
    low_y = min_point[1]
    vel = 30
    
    #run this loop while current position of the robot is not equal low_x and low_y 
    
    
    #the loop shouls stop when:
    
        # 1. low_x - 0.2 < curr_x2 < low_x + 0.2 
        
        # 2. low_y - 0.2 < curr_y2 < low_y + 0.2
    
    
    while(curr_x2 > (low_x - 0.2) or curr_x2 < (low_x + 0.2) or low_y - 0.2 < curr_y2 or  curr_y2 < low_y + 0.2): #add condition

        print("low_x:", low_x, "low_y:", low_y)

        print("curr_x:", curr_x2, "curr_y", curr_y2)
        
        #write conditions for wall following
        
        ##code here##
        
        if left_distance2 < 50:
            forward_right(vel)
       
        if left_distance2 > 200 and left_distance2 < 500: 
            forward_left(vel)
        if left_distance2 > 550:
            sharp_left(vel)
        else:
            forward(vel)
        
        kill()
    

    return low_x , low_y


# **Write the Main Function here**

if __name__ == '__main__':

    ep_robot = robot.Robot()
    
    ep_robot.initialize(conn_type = "ap")
    
    ep_chassis = ep_robot.chassis
    
    ep_sensor = ep_robot.sensor
    
    ep_led = ep_robot.led
    
    ep_led.set_led(comp=led.COMP_ALL, r=255, g=0, b=200, effect=led.EFFECT_ON)

    des_x = int(input("enter x coordinate = "))
    
    des_y = int(input("enter y coordinate = "))
    
    ep_sensor.sub_distance(freq = 10, callback = sub_data_handler)
    
    ep_chassis.sub_position(freq = 10, callback = sub_position_handler)
    
    ep_chassis.sub_attitude(freq = 10, callback = sub_attitude_info_handler)
    
    ep_sensor_adaptor = ep_robot.sensor_adaptor
    
    prev = 0.001
    
    distance_error = distance(des_x,des_y,0,0) 
    
    while (distance_error >= 0.2):

        front_distance = ep_sensor_adaptor.get_adc(id=1, port=1)

        if state == 0:
            
            print("In state 0")
            
            #call pid function and store distance_error, angle_error and prev

            ##code here##
            
            distance_error, angle_error,prev = pid(des_x, des_y, prev)
            
            #call movetogoal function 
            
            ##code here##
            movetogoal(distance_error, angle_error)
            
            #when object is detected state should be changed such that robot now starts wall following, curr_x and curr_y should be stored in variables called hit_x and hit_y respectively 
 
            
            
            #unsubscribe to position and distance 
            
            if(front_distance  > 700 and flag == 0):
                state = 1

                kill()
                
                ##code here##
                start_x = curr_x
                start_y = curr_y
                hit_x = start_x
                hit_y = start_y
                
                ep_chassis.unsub_position()
                ep_sensor.unsub_distance()

                flag = 1 

        elif state == 1:
            
            print("In state 1")

            #call wall following function 
            
            ##code here##
            
            state, distance_array = wallfollowing(start_x, start_y, des_x, des_y)
            
        elif state == 2:

            print("In state 2")

            #call movetomin function 
                        
            low_x, low_y = movetomin(distance_array)
            
            ep_chassis.unsub_position()

            break

    #from low point robot now needs to move to the desired goal position

    ep_chassis.sub_position(freq = 10, callback = sub_position_handler3) 
    
    print("curr_xy:", curr_x3, curr_y3)

    distance_error = distance(des_x - (hit_x + low_x), des_y - (hit_y + low_y), curr_x3, curr_y3) 
    
    print("distnce_error", distance_error)

    prev = 0.001
    
    while (distance_error >= 0.3):

        distance_error, angle_error , prev = pid1(des_x - (hit_x + low_x), des_y - (hit_y + low_y), prev)

        movetogoal(distance_error, angle_error)

    ep_chassis.unsub_position()
    
    ep_chassis.unsub_attitude()

    kill()
    
    ep_robot.close()
