#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from my_robot_interfaces.msg import HardwareStatus

class HardwareStatusPublisherNode(Node):

    def __init__(self):
        super().__init__("hw_status_publisher")

        self.hw_status_publisher_ = self.create_publisher(HardwareStatus, "status", 10)
        self.timer_ = self.create_timer(1,self.call_hw_status_pub)
        self.get_logger().info("Custom Publisher has been started!")

    def call_hw_status_pub(self):
        msg = HardwareStatus()
        msg.are_motor_ready = True
        msg.temperature = 34
        msg.debug_message = "it is noting"
        self.hw_status_publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = HardwareStatusPublisherNode()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()