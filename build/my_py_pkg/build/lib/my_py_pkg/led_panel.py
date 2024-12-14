#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from my_robot_interfaces.msg import LedStateArray
from my_robot_interfaces.srv import SetLed

class LedPanelNode(Node):

    def __init__(self):
        super().__init__("led_panel")

        self.led_states_ = [0,0,0]
        self.led_state_publisher_ = self.create_publisher(LedStateArray, "led_panel_state", 10)
        self.timer_ = self.create_timer(2,self.pub_led_panel_mode)
        self.get_logger().info("Server has been started")

        self.set_led_server_ = self.create_service(SetLed, "set_led", self.callback_set_led)

    def pub_led_panel_mode(self):
        msg = LedStateArray()
        msg.led_states = self.led_states_
        self.led_state_publisher_.publish(msg)

    def callback_set_led(self,request, response):
        led_number = request.led_number
        state = request.state

        if led_number > len(self.led_states_) or led_number <= 0:
            response.success = False
            return response

        if state not in [0,1]:
            response.success = False
            return response

        self.led_states_[led_number - 1] = state
        response.success = True
        self.pub_led_panel_mode()
        return response


def main(args=None):
    rclpy.init(args=args)
    node = LedPanelNode()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()