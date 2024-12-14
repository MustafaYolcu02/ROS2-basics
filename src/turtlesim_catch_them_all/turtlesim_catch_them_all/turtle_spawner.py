#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn
from geometry_msgs.msg import Point
import random
from functools import partial

class TurtleSpawnerNode(Node):

    def __init__(self):
        super().__init__("turtle_spawner")
        self.spawn_client = self.create_client(Spawn, "/spawn")
        self.counter = 1
        self.spawn_turtle_timer = self.create_timer(2.0, self.spawn_turtle)

        self.turtle_coord_pub = self.create_publisher(Point, "turtle_coordinates", 10)

        self.alive_turtle = []

    def spawn_turtle(self):
        while not self.spawn_client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for Server....")

        x = random.uniform(0.0, 11.0)
        y = random.uniform(0.0, 11.0)
        name = f"turtle_{self.counter}"
        self.counter += 1

        request = Spawn.Request()
        request.x = x
        request.y = y
        request.name = name

        self.alive_turtle.append(name)

        future = self.spawn_client.call_async(request)
        future.add_done_callback(partial(self.callback_call_spawn, x=x, y=y, name=name))

    def callback_call_spawn(self, future, x, y, name):
        try:
            response = future.result()
            self.get_logger().info(f"Turtle spawned successfully: {name} at ({x:.2f}, {y:.2f})")

            msg = Point()
            msg.x = x
            msg.y = y
            msg.z = 0.0
            self.turtle_coord_pub.publish(msg)
            self.get_logger().info(f"Published coordinates for {name}: ({x:.2f}, {y:.2f})")
            
        except Exception as e:
            self.get_logger().error("Service call failed %r" % (e,))

def main(args=None):
    rclpy.init(args=args)
    node = TurtleSpawnerNode()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()