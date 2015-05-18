#!/usr/bin/env python

import rospy
import kobuki_led_controller

if __name__ == '__main__':
    blinker = kobuki_led_controller.LedBlinker()
    blinker.loginfo('Initialized')
    blinker.spin()
    blinker.loginfo('Bye Bye')
