# Turtlebot Goal Navigation 
This package is developed for goal navigation on turtlebot3.

# Getting Started
Here, turtlebot3 hardware and simulation was used for testing  and implementation.\
For further information please follow; http://emanual.robotis.com/docs/en/platform/turtlebot3/overview/

# Prerequisites  & Test Environment
Ubuntu 16.04.6 LTS (Xenial) + ROS Kinetic + Turtlebot3 hardware

# Installation & Setup
For connecting the turtlebot3 hardware, please follow the issue ```Meet the real turtlebot``` in tier4.
simply clone this repo with command,```git clone git@fbe-gitlab.hs-weingarten.de:stud-amr/2019-ws-master/mg-183368_tier4.git ```\
make sure to install turtlebot3 navigation from,  ```https://github.com/ROBOTIS-GIT/turtlebot3.git```.\
Install and make teb planner at ```https://github.com/rst-tu-dortmund/teb_local_planner.git```

# Running the repo
1) Once you have connected your turtlebot with your pc with ```ssh pi@<ip_of_your_bot>```
2) For detailed instruction of launching and bringup, please follow the issue ```Meet the real turtlebot```
3) After this, we start our navigation & localization node with```roslaunch mg_183368_prj navigation.launch```
4) Then with ```2D Pose Estimate``` button on rviz, localization was improved followed by launching teleop node to drive the bot to the centre of the map ```roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch```
5) one can also test the setup with test goals with,```rosrun mg_183368_prj my_test_goals.py``` 
6) goal publisher is then started, make sure if your roscore is running ! 
7) Please double check if you are receiving the /goals topic.
8) At the end, run ```roslaunch mg_183368_prj goal_navigation.launch```


