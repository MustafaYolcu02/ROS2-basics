#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from my_robot_interfaces.srv import SetLed
from functools import partial

class BatteryNode(Node):

    def __init__(self):
        super().__init__("battery_node")
        self.battery_state_ = "full"
        self.last_time_battery_state_chanced_ = self.get_current_time_seconds()
        self.battery_timer_ = self.create_timer(0.1, self.check_battery_state)
        self.get_logger().info("Battery has been started")

    def get_current_time_seconds(self):
        secs, nsecs = self.get_clock().now().seconds_nanoseconds()
        return secs + nsecs/1000000000.0

    def check_battery_state(self):
        time_now = self.get_current_time_seconds()
        if self.battery_state_ == "full":
            if time_now - self.last_time_battery_state_chanced_ > 4.0 :
                self.battery_state_ = "empty"
                self.get_logger().info("Battery is empty!!")
                self.last_time_battery_state_chanced_ = time_now
                self.call_led_panel(3,1)
        else:
            if time_now -self.last_time_battery_state_chanced_ > 6.0:
                self.battery_state_ = "full"
                self.get_logger().info("Battery is full")
                self.last_time_battery_state_chanced_ = time_now
                self.call_led_panel(3,0)

    def call_led_panel(self, led_number, state):
        client = self.create_client(SetLed, "set_led")

        while not client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Service not available, waiting again...")

        request = SetLed.Request()
        request.led_number = led_number
        request.state = state

        future = client.call_async(request)
        future.add_done_callback(partial(self.callback_call_led_panel, led_number = led_number, state = state))

    def callback_call_led_panel(self,future, led_number, state):
        try:
            response = future.result()
            self.get_logger().info(f"Service call successful: {response.success}")
        except Exception as e:
            self.get_logger().error(f"Service call failed {e}" )


def main(args=None):
    rclpy.init(args=args)
    node = BatteryNode()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()