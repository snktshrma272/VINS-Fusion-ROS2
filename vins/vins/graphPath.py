#!/usr/bin/env python3
import rclpy
import matplotlib.pyplot as plt
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSDurabilityPolicy
from geometry_msgs.msg import PoseStamped

#subscribing topics
class GraphPath(Node):
    def __init__(self):
        super().__init__('graph_path')
        qos_profile = QoSProfile(depth=10)
        qos_profile.durability = QoSDurabilityPolicy.VOLATILE
        self.subscription = self.create_subscription(
            PoseStamped,
            '/mavros/local_position/pose',
            self.listener_callback,
            qos_profile)
        self.subscription
        self.x = []
        self.y = []
        self.z = [] 

    def listener_callback(self, msg):
        self.x.append(msg.pose.position.x)
        self.y.append(msg.pose.position.y)
        self.z.append(msg.pose.position.z)
        self.get_logger().info('x: "%s", y: "%s", z: "%s"' % (msg.pose.position.x, msg.pose.position.y, msg.pose.position.z))
        self.plot_graph()
        self.get_logger().info('Graph plotted successfully.')
    
    def plot_graph(self):
        plt.figure()
        plt.plot(self.x, self.y, label='Path')
        plt.xlabel('X Position')
        plt.ylabel('Y Position')
        plt.title('Path of the Robot')
        plt.legend()
        plt.grid()
        plt.pause(0.01)

def main(args=None):
    rclpy.init(args=args)
    graph_path = GraphPath()
    try:
        rclpy.spin(graph_path)
    except KeyboardInterrupt:
        pass
    finally:
        graph_path.destroy_node()
        rclpy.shutdown()
        plt.show()
        # Show the final plot
        plt.savefig('path_plot.png')
        plt.close()

main()