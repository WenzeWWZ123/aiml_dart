import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction, SetEnvironmentVariable
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    pkg_gazebo_ros = FindPackageShare("gazebo_ros")

    urdf_file = os.path.expanduser(
        "~/ros2_ws/src/dart_description/urdf/aiml_dart_flat_clean.urdf"
    )

    with open(urdf_file, "r") as f:
        robot_desc_text = f.read()

    robot_description = {
        "robot_description": ParameterValue(
            robot_desc_text,
            value_type=str
        )
    }

    env = SetEnvironmentVariable(
        name="GAZEBO_ROS_CONTROL_USE_PARAM_SERVER",
        value="false"
    )

    rsp = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[robot_description],
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [pkg_gazebo_ros, "/launch/gazebo.launch.py"]
        )
    )

    spawn = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=[
            "-entity", "dart_robot",
            "-topic", "robot_description",
            "-x", "0",
            "-y", "0",
            "-z", "0.1",
        ],
        output="screen",
    )

    delayed_spawn = TimerAction(
        period=3.0,
        actions=[spawn],
    )

    return LaunchDescription([
        env,
        gazebo,
        rsp,
        delayed_spawn,
    ])