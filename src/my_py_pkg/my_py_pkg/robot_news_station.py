#!/usr/bin/env python3


import rclpy
from rclpy.node import Node
from example_interfaces.msg import String

class RobotNewsStationNode(Node):

    def __init__(self):
        super().__init__("robot_news_station")

        #self.publisher_ = self.create_publisher(String, "robot_news", 10)
        #self.timer_ = self.create_timer(1, self.publish_news)
        #self.get_logger().info("Robot News Station has been started!")

        self.declare_parameter('robot_name', 'DefaultBot')
        self.robot_name = self.get_parameter('robot_name').get_parameter_value().string_value
        self.publisher = self.create_publisher(String, 'robot_haberleri', 10)
        self.timer = self.create_timer(1.0, self.robot_new)

    def publish_news(self):
        msg = String()
        msg.data = "Hello"
        self.publisher_.publish(msg)
    
    def robot_new(self):
        message = String()
        message.data = f"Hi, this is {self.robot_name} from the Robot News Station!"
        self.publisher.publish(message)


def main(args=None):
    rclpy.init(args=args)
    node = RobotNewsStationNode()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()