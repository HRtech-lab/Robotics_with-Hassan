#Importing libraries
import robomaster
import time
import readchar
from robomaster import robot
import keyboard

slp = 0.1 #important variable
# **Move the Robot forward using ep_chassis wheels function** 

def forward(vel):
    ##code here##
    ep_chassis.drive_wheels(w1 = vel, w2 = vel, w3 = vel, w4 = vel)
    time.sleep(slp)
    kill()

# **Move the Robot back using ep_chassis wheels function**

def backward(vel):
    ep_chassis.drive_wheels(w1 = -vel, w2 = -vel, w3 = -vel, w4 = -vel)
    time.sleep(slp)
    kill()


# **Move the Robot right while moving forward using ep_chassis wheels function**




def forward_right(vel):
    ##code here##
    ep_chassis.drive_wheels(w1 = -vel, w2 = vel, w3 = vel, w4 = vel)
    time.sleep(slp)
    kill()


# **Move the Robot right while moving backwards using ep_chassis wheel function**

# In[ ]:



def backward_right(vel):
    #code here##
    ep_chassis.drive_wheels(w1 = -vel, w2 = -vel, w3 = -vel, w4 = vel)
    time.sleep(slp)
    kill()


# **Move the Robot left while moving forward using ep_chassis wheels function**

# In[ ]:


def forward_left(vel):
    ##code here##
    ep_chassis.drive_wheels(w1 = vel, w2 = -vel, w3 = vel, w4 = vel)
    time.sleep(slp)
    kill()


# **Move the Robot left while moving backwards using ep_chassis wheel function**

# In[ ]:


def backward_left(vel):
    ep_chassis.drive_wheels(w1 = -vel, w2 = -vel, w3 = vel, w4 = -vel)
    time.sleep(slp)
    kill()


# **Make the Robot move right sharply using ep_chassis wheels function**

# In[ ]:


def sharp_right(vel):
    ##code here##
    ep_chassis.drive_wheels(w1 = -vel, w2 = vel, w3 = -vel, w4 = vel)
    time.sleep(slp)
    kill()


# **Make the Robot move left sharply using ep_chassis wheels function**

# In[ ]:


def sharp_left(vel):
    ##code here##
    ep_chassis.drive_wheels(w1 = vel, w2 = -vel, w3 = vel, w4 = -vel)
    time.sleep(slp)
    kill()


# **Stop the robot**

# In[ ]:


def kill():
    ep_chassis.drive_wheels(w1 = 0, w2 = 0, w3 = 0, w4 = 0)


# **Write the main function here**

# In[ ]:


if __name__ == '__main__':

    #initialize the robot 
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")

    #create chassis object

    ep_chassis = ep_robot.chassis

    #velocity parameter, keep the velocity low at first when testing
    vel = 0.2


    while(1):

      #use readchar python library to get keyboard key event

     #add three levels of robot speed based on keyboard event

     #add all robot movement control based on keyboard events

     #add a condition that breaks the while loop when a keyboard key is pressed
    
      ##code here##

      if keyboard.is_pressed("w"):
        forward(vel)
      if keyboard.is_pressed("s"):
        backward(vel)
      if keyboard.is_pressed("a"):
        sharp_left(vel)
      if keyboard.is_pressed("d"):
        sharp_right(vel)
      if keyboard.is_pressed("q"):
        forward_left(vel)
      if keyboard.is_pressed("e"):
        forward_right(vel)
      if keyboard.is_pressed("z"):
        backward_left(vel)
      if keyboard.is_pressed("c"):
        backward_right(vel)
      
      if keyboard.is_pressed("p"):
        break

ep_robot.close()
