import robomaster
from robomaster import robot
import time
import matplotlib.pyplot as plt


# **Create a callback function that appends the IR sensor value distance array. Make sure to make the variable global so it can be used later in the main function**
# **Also print the values for visualization**

distance =  []
def sub_data_handler(sub_info):
    ##code here##
    distance.append(sub_info)
    print(sub_info)


# **Write the main function here**



if __name__ == '__main__':

    #initliaze the robot
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")
    
    ep_chassis = ep_robot.chassis
    
    #create sensor object
    ep_sensor = ep_robot.sensor

    #create callback
    ep_sensor.sub_distance(freq=5, callback=sub_data_handler)

    while (1):
      
      #move the robot forward
      #append the IR sensor values in an array
      #plot these values using matplotlib 
      ep_chassis.move(x=0, y=0, z=0, xy_speed=0).wait_for_completed()
      
      if len(distance) > 3:
        break
    ep_sensor.unsub_distance()
    ep_robot.close()
    plt.plot(distance)
    plt.title("Distance from nearest obstacle (y) against time in seconds (x)")
    plt.show()  
ep_chassis.move(x=0.1, y=0, z=0, xy_speed=0.02).wait_for_completed()
