#----------------------------------------------------------------
# Generated CMake target import file for configuration "Debug".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "my_robot_interfaces::my_robot_interfaces__rosidl_generator_c" for configuration "Debug"
set_property(TARGET my_robot_interfaces::my_robot_interfaces__rosidl_generator_c APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(my_robot_interfaces::my_robot_interfaces__rosidl_generator_c PROPERTIES
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/lib/libmy_robot_interfaces__rosidl_generator_c.so"
  IMPORTED_SONAME_DEBUG "libmy_robot_interfaces__rosidl_generator_c.so"
  )

list(APPEND _cmake_import_check_targets my_robot_interfaces::my_robot_interfaces__rosidl_generator_c )
list(APPEND _cmake_import_check_files_for_my_robot_interfaces::my_robot_interfaces__rosidl_generator_c "${_IMPORT_PREFIX}/lib/libmy_robot_interfaces__rosidl_generator_c.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
