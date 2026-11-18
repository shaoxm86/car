#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseWithCovarianceStamped
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32
import math

class AmclOdomCompare(Node):
    def __init__(self):
        super().__init__('amcl_odom_compare')
        self.amcl_pose = None
        self.odom_pose = None

        # 新增：发布误差话题
        self.error_pub = self.create_publisher(Float32, '/amcl_odom_error', 10)

        self.sub_amcl = self.create_subscription(
            PoseWithCovarianceStamped,
            '/amcl_pose',
            self.amcl_callback,
            10
        )
        self.sub_odom = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )
        self.timer = self.create_timer(0.1, self.timer_callback)

    def amcl_callback(self, msg):
        self.amcl_pose = (msg.pose.pose.position.x, msg.pose.pose.position.y)

    def odom_callback(self, msg):
        self.odom_pose = (msg.pose.pose.position.x, msg.pose.pose.position.y)

    def timer_callback(self):
        if self.amcl_pose and self.odom_pose:
            dx = self.amcl_pose[0] - self.odom_pose[0]
            dy = self.amcl_pose[1] - self.odom_pose[1]
            error = math.sqrt(dx**2 + dy**2)

            # 发布误差值
            msg = Float32()
            msg.data = error
            self.error_pub.publish(msg)

            self.get_logger().info(f'AMCL vs Odom Error: {error:.3f} m')

def main(args=None):
    rclpy.init(args=args)
    node = AmclOdomCompare()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
