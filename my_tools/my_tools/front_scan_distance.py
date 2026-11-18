#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import math

class FrontScanReader(Node):
    def __init__(self):
        super().__init__('front_scan_reader')
        self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )

    def scan_callback(self, msg):
        distances = []
        for i, r in enumerate(msg.ranges):
            angle_deg = math.degrees(msg.angle_min + i * msg.angle_increment)
            if -5.0 <= angle_deg <= 5.0:  # 前方 ±5°
                if r < float('inf'):
                    distances.append(r)
        if distances:
            nearest = min(distances)
            self.get_logger().info(f"Front obstacle distance: {nearest:.2f} m")
        else:
            self.get_logger().info("Front obstacle: None detected")

def main(args=None):
    rclpy.init(args=args)
    node = FrontScanReader()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        # 注意：不调用 rclpy.shutdown()，这样脚本退出不影响其他ROS节点

if __name__ == '__main__':
    main()
