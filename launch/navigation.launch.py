# Copyright (c) 2024 José Miguel Guerrero Hernández
#
# This file is licensed under the terms of the MIT license.
# See the LICENSE file in the root of this repository

import os
import yaml

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    sim_dir = get_package_share_directory('tiago_simulator')
    tiago_2dnav_dir = get_package_share_directory('tiago_2dnav')
    nav2_bringup_dir = get_package_share_directory("nav2_bringup")
    config = os.path.join(sim_dir, 'config', 'params.yaml')

    with open(config, "r") as stream:
        try:
            conf = (yaml.safe_load(stream))

        except yaml.YAMLError as exc:
            print(exc)

    world_name = conf['tiago_simulator']['world']

    nav2_bringup_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup_dir, "launch", "bringup_launch.py")
        ),
        launch_arguments={
            "params_file": os.path.join(
                tiago_2dnav_dir, "params", "tiago_nav_public_sim.yaml"
            ),
            "map": os.path.join(sim_dir, 'maps', world_name + '.yaml'),
            "use_sim_time": "True",
        }.items(),
    )

    rviz_bringup_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup_dir, "launch", "rviz_launch.py")
        ),
        launch_arguments={
            "rviz_config": os.path.join(
                tiago_2dnav_dir, "config", "rviz", "navigation.rviz"
            ),
        }.items(),
    )

    ld = LaunchDescription()

    ld.add_action(nav2_bringup_launch)
    ld.add_action(rviz_bringup_launch)

    return ld
