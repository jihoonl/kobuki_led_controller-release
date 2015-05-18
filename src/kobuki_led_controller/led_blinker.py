"""
    Blinks Kobuki LEDS!!!
"""
import rospy
import threading
from kobuki_msgs.msg import Led

STATE_OFF    = 0
STATE_OK     = 1
STATE_ERROR  = 2

class LedBlinker(object):
    
    __led1 = '/mobile_base/commands/led1'
    __led2 = '/mobile_base/commands/led2'

    def __init__(self):
        self.rate = rospy.get_param('~rate', 3)

        self.pub = {}
        self.pub['led1'] = rospy.Publisher(self.__led1, Led, queue_size=1)
        self.pub['led2'] = rospy.Publisher(self.__led2, Led, queue_size=1)

        self._last_blink_led = 2
        self._state = STATE_OFF
        self.thread = threading.Thread(target=self._blinker)
        self._lock = threading.Lock()

    def start(self):
        self.thread.start()

    def stop(self):
        self.thread.join()

    def spin(self):
        self.thread.start()
        rospy.spin()
        # Teminating..
        self.pub['led1'].publish(Led.BLACK)
        self.pub['led2'].publish(Led.BLACK)

    def _blinker(self):
        r = rospy.Rate(self.rate)
        while not rospy.is_shutdown(): 
            self._last_blink_led = (self._last_blink_led % 2 ) + 1

            self._lock.acquire()
            if self._state == STATE_OFF:
                led1 = Led.BLACK
                led2 = Led.BLACK
            elif self._state == STATE_OK:
                led1 = Led.BLACK if self._last_blink_led == 1 else Led.GREEN
                led2 = Led.GREEN if self._last_blink_led == 1 else Led.BLACK
            elif self._state == STATE_ERROR:
                 led1 = Led.BLACK if self._last_blink_led == 1 else Led.RED
                 led2 = Led.RED if self._last_blink_led == 1 else Led.BLACK
            self._lock.release()

            self.pub['led1'].publish(led1)
            self.pub['led2'].publish(led2)
            r.sleep()

    def set_on_error(self):
        self._lock.acquire()
        self._state = STATE_ERROR
        self._lock.release()

    def set_on_ok(self):
        self._lock.acquire()
        self._state = STATE_OK
        self._lock.release()

    def set_on_off(self):
        self._lock.acquire()
        self._state = STATE_OFF
        self._lock.release()
