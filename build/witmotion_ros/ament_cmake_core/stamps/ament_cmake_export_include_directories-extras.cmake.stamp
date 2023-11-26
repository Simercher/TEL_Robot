# generated from ament_cmake_export_include_directories/cmake/ament_cmake_export_include_directories-extras.cmake.in

set(_exported_include_dirs "/opt/ros/foxy/include;/usr/include/eigen3;/usr/include/aarch64-linux-gnu/qt5/;/usr/include/aarch64-linux-gnu/qt5/QtCore;/usr/lib/aarch64-linux-gnu/qt5//mkspecs/linux-g++;/usr/include/aarch64-linux-gnu/qt5/QtSerialPort")

# append include directories to witmotion_ros_INCLUDE_DIRS
# warn about not existing paths
if(NOT _exported_include_dirs STREQUAL "")
  find_package(ament_cmake_core QUIET REQUIRED)
  foreach(_exported_include_dir ${_exported_include_dirs})
    if(NOT IS_DIRECTORY "${_exported_include_dir}")
      message(WARNING "Package 'witmotion_ros' exports the include directory '${_exported_include_dir}' which doesn't exist")
    endif()
    normalize_path(_exported_include_dir "${_exported_include_dir}")
    list(APPEND witmotion_ros_INCLUDE_DIRS "${_exported_include_dir}")
  endforeach()
endif()
