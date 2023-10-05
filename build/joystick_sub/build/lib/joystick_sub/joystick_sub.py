import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from sensor_msgs.msg import Joy


class Joystick_sub(Node):

    def __init__(self):
        super().__init__('joystick_sub')
        self.subscription = self.create_subscription(
            Joy,
            'joy',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        for i in msg.buttons:
            if i:
                self.get_logger().info('"%s"' % i)
        for i in msg.axes:
            if i:
                self.get_logger().info('"%s"' % i)

def main(args=None):
    rclpy.init(args=args)

    joystick_sub = Joystick_sub()

    rclpy.spin(joystick_sub)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    joystick_sub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()