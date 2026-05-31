#ifndef MICROTRACTOR_CONTROL__MICROTRACTOR_SYSTEM_HPP_
#define MICROTRACTOR_CONTROL__MICROTRACTOR_SYSTEM_HPP_

#include <memory>
#include <string>
#include <vector>

#include "hardware_interface/handle.hpp"
#include "hardware_interface/hardware_info.hpp"
#include "hardware_interface/system_interface.hpp"
#include "hardware_interface/types/hardware_interface_return_values.hpp"
#include "rclcpp/clock.hpp"
#include "rclcpp/duration.hpp"
#include "rclcpp/macros.hpp"
#include "rclcpp/time.hpp"
#include "rclcpp_lifecycle/node_interfaces/lifecycle_node_interface.hpp"
#include "rclcpp_lifecycle/state.hpp"

#include "std_msgs/msg/float32.hpp"

namespace microtractor_control{

class MicrotractorSystemHardware : public hardware_interface::SystemInterface {
    public:
        RCLCPP_SHARED_PTR_DEFINITIONS(MicrotractorSystemHardware);

        hardware_interface::CallbackReturn on_init(
            const hardware_interface::HardwareInfo & info) override;
        
        std::vector<hardware_interface::StateInterface> export_state_interfaces() override;

        std::vector<hardware_interface::CommandInterface> export_command_interfaces() override;
/*
        hardware_interface::CallbackReturn on_activate(
            const rclcpp_lifecycle::State & previous_state) override;

        hardware_interface::CallbackReturn on_deactivate(
            const rclcpp_lifecycle::State & previous_state) override;*/

        hardware_interface::return_type read(
            const rclcpp::Time & time, const rclcpp::Duration & period) override;

        hardware_interface::return_type write(
            const rclcpp::Time & time, const rclcpp::Duration & period) override;
    
    private:
        /*std::vector<double> hw_commands_;
        std::vector<double> hw_velocities_;*/
        double cmd_vel_IZQ;
        double cmd_vel_DER;

        std::shared_ptr<rclcpp::Node> node;
        rclcpp::Publisher<std_msgs::msg::Float32>::SharedPtr pub_vel_IZQ;
        rclcpp::Publisher<std_msgs::msg::Float32>::SharedPtr pub_vel_DER;

};

}


#endif