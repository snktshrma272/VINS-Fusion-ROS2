#include <chrono>
#include <functional>
#include <iostream>
#include <memory>
#include <string>
#include <vector>

#include "rclcpp/rclcpp.hpp"
#include "rclcpp/serialization.hpp"
#include "rosbag2_transport/reader_writer_factory.hpp"
#include "geometry_msgs/msg/pose_stamped.hpp"

using namespace std::chrono_literals;

class readPoseNode : public rclcpp::Node {
    public:
        readPoseNode(const std::string& bag_filename) : Node("readPoseNode") {
            publisher_ = this->create_publisher<geometry_msgs::msg::PoseStamped>("/test/pose",10);
            timer_ = this->create_wall_timer(
                100ms, std::bind(&readPoseNode::timer_callback, this)
            );

            rosbag2_storage::StorageOptions storage_options;

            storage_options.uri = bag_filename;

            reader_ = rosbag2_transport::ReaderWriterFactory::make_reader(storage_options);
            reader_->open(storage_options);
        }

    private:
        void timer_callback()
        {
            while (reader_->has_next()) {
                rosbag2_storage::SerializedBagMessageSharedPtr msg = reader_->read_next();

                if (msg->topic_name != "/mavros/local_position/pose") {
                    continue;
                }
        
                rclcpp::SerializedMessage serialized_msg(*msg->serialized_data);
                geometry_msgs::msg::PoseStamped::SharedPtr ros_msg = std::make_shared<geometry_msgs::msg::PoseStamped>();
        
                serialization_.deserialize_message(&serialized_msg, ros_msg.get());
        
                publisher_->publish(*ros_msg);
                std::cout << '(' << ros_msg->pose.position.x << ", " << ros_msg->pose.position.y << ", " << ros_msg->pose.position.z << ")\n";
    
                break;
            }
        }
        
        
        rclcpp::TimerBase::SharedPtr timer_;
        rclcpp::Publisher<geometry_msgs::msg::PoseStamped>::SharedPtr publisher_;
        
        rclcpp::Serialization<geometry_msgs::msg::PoseStamped> serialization_;
        std::unique_ptr<rosbag2_cpp::Reader> reader_;
};
      
      int main(int argc, char ** argv)
      {
        if (argc != 2) {
          std::cerr << "Usage: " << argv[0] << " <bag>" << std::endl;
          return 1;
        }
      
        rclcpp::init(argc, argv);
        rclcpp::spin(std::make_shared<readPoseNode>(argv[1]));
        rclcpp::shutdown();
      
        return 0;
      }