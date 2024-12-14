#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn
from geometry_msgs.msg import Point
import random

class TurtleSpawnerNode(Node):

    def __init__(self):
        super().__init__("turtle_spawner")
        self.client_ = self.create_client(Spawn, "/spawn")
        self.counter = 1

        self.list_turtle = []

        self.spawn_turtle_timer = self.create_timer(2.0, self.spawn_turtle)

        self.coord_publisher = self.create_publisher(Point, "/spawned_turtle_coords", 10)

    def spawn_turtle(self):
        while not self.client_.wait_for_service(1.0):
            self.get_logger().warn("Waiting for Server....")

        x = random.uniform(0.0, 11.0)
        y = random.uniform(0.0, 11.0)

        name = f"turtle_{self.counter}"
        self.counter += 1

        request = Spawn.Request()
        request.x = x
        request.y = y
        request.name = name

        future = self.client_.call_async(request)
        rclpy.spin_until_future_complete(self, future)

        if future.result() is not None:
            self.get_logger().info(f"Turtle spawned: {name} at ({x:.2f}, {y:.2f})")
            self.list_turtle.append({"name": name, "x": x, "y": y})
            point_msg = Point()
            point_msg.x = x
            point_msg.y = y
            point_msg.z = 0.0
            self.coord_publisher.publish(point_msg)
        else:
            self.get_logger().info("Failed to call /spaw service")




def main(args=None):
    rclpy.init(args=args)
    node = TurtleSpawnerNode()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()