cmake_minimum_required(VERSION 2.8.3)
project(kobuki_led_controller)

find_package(catkin REQUIRED)

catkin_python_setup()
catkin_package()

install(PROGRAMS
    scripts/kobuki_led_blinker.py
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
