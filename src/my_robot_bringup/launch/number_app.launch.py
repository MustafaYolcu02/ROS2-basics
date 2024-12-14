from launch import LaunchDescription
from launch_ros.actions import Node



def generate_launch_description():
    ld = LaunchDescription()

    number_publisher_node = Node(
        package= "my_py_pkg", 
        executable= "num_pub", 
        name= "my_number_publisher", 
        remappings= [
            ("number", "my_number")
        ]
    )

    number_counter_node = Node(
        package= "my_py_pkg", 
        executable= "num_sub", 
        name= "my_number_counter",
        remappings= [
            ("number", "my_number")
        ]
    )


    ld.add_action(number_publisher_node)
    ld.add_action(number_counter_node)
    return ld