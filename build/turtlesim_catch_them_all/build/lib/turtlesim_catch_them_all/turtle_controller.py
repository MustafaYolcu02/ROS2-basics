#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point
import math

class TurtleControlNode(Node):

    def __init__(self):
        super().__init__("turtle_controller")
        self.pose = Pose()
        self.target_x = 0.0
        self.target_y = 0.0

        self.pose_subscriber = self.create_subscription(Pose, "turtle1/pose", self.pose_callback, 10)
        self.twist_pub = self.create_publisher(Twist, "turtle1/cmd_vel", 10)

        self.coord_subscriber = self.create_subscription(Point, "/spawned_turtle_coords", self.coord_callback, 10)

        self.twist_pub_timer = self.create_timer(0.1, self.control_loop)

    def pose_callback(self, msg):
        self.pose = msg

    def coord_callback(self,msg):
        msg = Point()
        self.target_x = msg.x
        self.target_y = msg.y

    def control_loop(self):
        dx = self.target_x - self.pose.x
        dy = self.target_y - self.pose.y

        distance = math.sqrt(dx**2 + dy**2)

        angle_to_turtle = math.atan2(dy, dx)
        angle_diff = angle_to_turtle - self.pose.theta
        angle_diff = (angle_diff + math.pi) % (2 * math.pi) - math.pi

        move_msg = Twist()
        move_msg.linear.x = min(1.0, distance)
        move_msg.angular.z = min(1.0, max(-1.0, angle_diff))

        self.twist_pub.publish(move_msg)

        if distance < 0.1:
            self.get_logger().info("Target Reached.")
            self.stop_turtle()
            return

    def stop_turtle(self):
        stop_msg = Twist()

        stop_msg.linear.x = 0.0
        stop_msg.angular.z = 0.0

        self.twist_pub.publish(stop_msg)



def main(args=None):
    rclpy.init(args=args)
    node = TurtleControlNode()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()