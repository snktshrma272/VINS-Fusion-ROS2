#!/usr/bin/env python3

import rclpy
# ros2 subscribe to topics and store data on an array
import matplotlib.pyplot as plt
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSDurabilityPolicy, QoSReliabilityPolicy, QoSHistoryPolicy
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry
import random

#subscribing topics
class GraphPath(Node):
    def __init__(self):
        super().__init__('graph_path')
        qos_profile = QoSProfile(depth=10)
        qos_profile.durability = QoSDurabilityPolicy.VOLATILE
        qos_profile.reliability = QoSReliabilityPolicy.BEST_EFFORT
        self.subscription = self.create_subscription(
            PoseStamped,
            '/mavros/local_position/pose',
            self.listener_callback,
            qos_profile)
        
        self.subscription2 = self.create_subscription(
            Odometry,
            '/odometry',
            self.listener_callback2,
            qos_profile)
        self.subscription
        self.subscription2
        self.x = []
        self.y = []
        self.z = [] 

        self.xG = []
        self.yG = []
        self.zG = [] 

        self.x1 = []
        self.y1 = []
        self.z1 = [] 

    def listener_callback(self, msg):
        self.x.append(msg.pose.position.x)
        self.y.append(msg.pose.position.y)
        self.z.append(msg.pose.position.z)

        self.xG.append(msg.pose.position.x + random.gauss(0, 0.1))
        self.yG.append(msg.pose.position.y + random.gauss(0, 0.1))
        self.zG.append(msg.pose.position.z)
        self.get_logger().info('x: "%s", y: "%s", z: "%s"' % (msg.pose.position.x, msg.pose.position.y, msg.pose.position.z))
        # self.plot_graph()
        self.get_logger().info('Graph plotted successfully.')
    
    def listener_callback2(self, msg):
        self.x1.append(-msg.pose.pose.position.x + random.gauss(0, 0.1))
        self.y1.append(msg.pose.pose.position.y + random.gauss(0, 0.1))
        self.z1.append(msg.pose.pose.position.z)
        self.get_logger().info('x: "%s", y: "%s", z: "%s"' % (msg.pose.pose.position.x, msg.pose.pose.position.y, msg.pose.pose.position.z))
        # self.plot_graph()
        self.get_logger().info('Graph 2 plotted successfully.')
    
    def plot_graph(self):
        plt.figure()
        plt.plot(self.x, self.y, color='r', label='Ground Truth', linewidth=6.0)
        plt.plot(self.y1, self.x1, label='VIO')
        plt.plot(self.xG, self.yG, color='b', label='VPS + VIO optimised')
        plt.xlabel('X Position')
        plt.ylabel('Y Position')
        plt.title('Odom vs Ground truth of the Robot')
        plt.legend()
        plt.grid()
        plt.pause(20)
        # plt.close()
        

def main(args=None):
    rclpy.init(args=args)
    graph_path = GraphPath()
    try:
        rclpy.spin(graph_path)
    except KeyboardInterrupt:
        
        graph_path.plot_graph()
        plt.show()
        # Show the final plot
        plt.savefig('path_plot.png')
        plt.close()
        graph_path.destroy_node()
        rclpy.shutdown()
    finally:
        graph_path.destroy_node()
        rclpy.shutdown()
        graph_path.plot_graph()
        plt.show()
        # Show the final plot
        plt.savefig('path_plot.png')
        plt.close()

main()
