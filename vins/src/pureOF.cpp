#include <stdio.h>
#include <queue>
#include <map>
#include <thread>
#include <mutex>
#include <rclcpp/rclcpp.hpp>
#include <cv_bridge/cv_bridge.h>
#include <opencv2/opencv.hpp>

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    auto node = rclcpp::Node::make_shared("optical_flow_estimation");
    return 0;
}
