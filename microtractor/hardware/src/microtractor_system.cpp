#include "microtractor_control/microtractor_system.hpp"

#include <chrono>
#include <cmath>
#include <cstddef>
#include <iomanip>
#include <limits>
#include <memory>
#include <sstream>
#include <vector>

#include "hardware_interface/lexical_casts.hpp"
#include "hardware_interface/types/hardware_interface_type_values.hpp"
#include "rclcpp/rclcpp.hpp"

#include "std_msgs/msg/float32.hpp"

#define MAX_VEL 1.0

using namespace microtractor_control;

hardware_interface::CallbackReturn MicrotractorSystemHardware::on_init(const hardware_interface::HardwareInfo & info){

    if (hardware_interface::SystemInterface::on_init(info) != hardware_interface::CallbackReturn::SUCCESS) {
        return hardware_interface::CallbackReturn::ERROR;
    }   

    cmd_vel_IZQ = 0.0;
    cmd_vel_DER = 0.0;

    node = std::make_shared<rclcpp::Node>("microtractor_hardware_node");
    pub_vel_DER = node->create_publisher<std_msgs::msg::Float32>("/cmd_vel/PWM/DER", 10);
    pub_vel_IZQ = node->create_publisher<std_msgs::msg::Float32>("/cmd_vel/PWM/IZQ", 10);

    return hardware_interface::CallbackReturn::SUCCESS;
    }

std::vector<hardware_interface::StateInterface> MicrotractorSystemHardware::export_state_interfaces(){
    //Bucle abierto
    return {};
}

std::vector<hardware_interface::CommandInterface> MicrotractorSystemHardware::export_command_interfaces(){
    std::vector<hardware_interface::CommandInterface> command_interfaces;
    for (auto i = 0u; i < info_.joints.size(); i++) {
        if(info_.joints[i].name == "right_attack_pinion_joint"){
            command_interfaces.emplace_back(hardware_interface::CommandInterface(
                info_.joints[i].name, hardware_interface::HW_IF_VELOCITY, &cmd_vel_DER));
        }
        else if(info_.joints[i].name == "left_attack_pinion_joint"){
            command_interfaces.emplace_back(hardware_interface::CommandInterface(
                            info_.joints[i].name, hardware_interface::HW_IF_VELOCITY, &cmd_vel_IZQ));
        }
    }

    return command_interfaces;
}
/*
hardware_interface::CallbackReturn MicrotractorSystemHardware::on_activate(
    const rclcpp_lifecycle::State & previous_state){

    }

hardware_interface::CallbackReturn on_deactivate(
    const rclcpp_lifecycle::State & previous_state){

    }*/

hardware_interface::return_type MicrotractorSystemHardware::read(
    const rclcpp::Time & time, const rclcpp::Duration & period){
        // Bucle abierto
        return hardware_interface::return_type::OK;
    }

hardware_interface::return_type MicrotractorSystemHardware::write(
    const rclcpp::Time & time, const rclcpp::Duration & period){
        auto msg_IZQ = std_msgs::msg::Float32();
        msg_IZQ.data = cmd_vel_IZQ / MAX_VEL;
        pub_vel_IZQ->publish(msg_IZQ);

        auto msg_DER = std_msgs::msg::Float32();
        msg_DER.data = cmd_vel_DER / MAX_VEL;
        pub_vel_DER->publish(msg_DER);

        return hardware_interface::return_type::OK;
    }

#include "pluginlib/class_list_macros.hpp"
PLUGINLIB_EXPORT_CLASS(microtractor_control::MicrotractorSystemHardware, hardware_interface::SystemInterface)
