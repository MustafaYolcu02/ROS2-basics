#!/usr/bin/env python3


import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64
from example_interfaces.srv import SetBool

class NumberSub(Node):

    def __init__(self):
        super().__init__("num_count")
        
        self.subscription_ = self.create_subscription(Int64, "number", self.callback_counter, 10)
        self.get_logger().info("Counter has been started")
        self.total_count = 0
        
        self.publisher_ = self.create_publisher(Int64, "number_counter", 10)
        self.timer_ = self.create_timer(1, self.pub_counter)
        
        self.reset_couter_service_ = self.create_service(SetBool,"reset_counter", self.callback_reset_counter)

    def pub_counter(self):
        mesaj = Int64()
        mesaj.data = self.total_count
        self.publisher_.publish(mesaj)
        
    def callback_counter(self, msg):
        #self.get_logger().info(f"Received message with data: {str(msg.data)}")
        self.total_count += msg.data
    
    def callback_reset_counter(self,request,response):
        if request.data:
            self.total_count = 0
            response.success = True
            response.message = "Counter has been reset"
        else:
            response.success = False
            response.message = "Counter has not been reset"
        return response

def main(args=None):
    rclpy.init(args=args)
    node = NumberSub()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()