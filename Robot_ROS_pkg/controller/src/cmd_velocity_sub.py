#!/usr/bin/env python3

from pynq import Overlay
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
from geometry_msgs.msg import Twist

class ListenerNode(Node):
    def __init__(self):
        super().__init__('wheel_controller')
        self.overlay = Overlay("/home/xilinx/catkin_ws/src/controller/src/driver.bit")
        self.controller_right = self.overlay.controller_PWM_0
        self.controller_left  = self.overlay.controller_PWM_1
        print("bitstream load")
        self.subscription_ = self.create_subscription(Twist, 'cmd_vel', self.velocity_callback, 10) 
        self.subscription_

    def velocity_callback(self,data):
    # Statics
        wheelbase_radius_meters = 0.19685
        encoder_postions_per_meter = 300.7518
        global currentLeftWheelSpeed
        global currentRightWheelSpeed

        print("callback")
        
        if data.linear.x:
         currentLeftWheelSpeed = encoder_postions_per_meter * data.linear.x
         currentRightWheelSpeed = encoder_postions_per_meter * data.linear.x

        if data.angular.z > 0:
         currentRightWheelSpeed += encoder_postions_per_meter * data.angular.z * wheelbase_radius_meters
         currentLeftWheelSpeed -= encoder_postions_per_meter * data.angular.z * wheelbase_radius_meters
        elif data.angular.z < 0:
         currentRightWheelSpeed += encoder_postions_per_meter * data.angular.z * wheelbase_radius_meters
         currentLeftWheelSpeed -= encoder_postions_per_meter * data.angular.z * wheelbase_radius_meters

        print("Right: "+str(currentRightWheelSpeed) +"   Left:"+str(currentLeftWheelSpeed))
        self.controller_right.write(0x00, int(currentLeftWheelSpeed))
        self.controller_left.write(0x00, int(currentRightWheelSpeed))
 

    def listener_callback(self, msg):
        velocity  = msg.data
        self.get_logger().info('Received: %d' % msg.data)
        print(str(velocity))
        self.controller_right.write(0x00, velocity)



def main(args=None):
    rclpy.init(args=args)
    node = ListenerNode()
    rclpy.spin(node)
    node.destroy_node()
    print("Node destroy")
    rclpy.shutdown()

if __name__ == '__main__':
    main()
