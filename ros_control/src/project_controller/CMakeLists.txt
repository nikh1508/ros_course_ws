cmake_minimum_required(VERSION 3.0.2)
project(project_controller)

find_package(catkin REQUIRED COMPONENTS
  controller_interface
  hardware_interface
  pluginlib
  roscpp
)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES project_controller
#  CATKIN_DEPENDS controller_interface hardware_interface pluginlib roscpp
#  DEPENDS system_lib
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

add_library(project_controller_lib src/my_controller.cpp)
target_link_libraries(project_controller_lib ${catkin_LIBRARIES})