import roslaunch

package = 'turtlesim'
executable = 'turtlesim_node'
node = roslaunch.core.Node(package, executable)

launch = roslaunch.scriptapi.ROSLaunch()
launch.start()

process = launch.launch(node)
print process.is_alive()
