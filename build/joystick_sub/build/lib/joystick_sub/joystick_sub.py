import rclpy
from rclpy.node import Node

from std_msgs.msg import Int8, Int32
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
        
        # publisher
        self.publisher_ = self.create_publisher(Int8, 'topic', 10)
        timer_period = 0.01  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = Int8()
        self.count = 0

    def listener_callback(self, msg):
        for i in msg.buttons:
            if i:
                self.get_logger().info('"%s"' % i)
        for i in msg.axes:
            if i:
                # if self.count % 3 == 1:
                self.i.data = round(i*100)
                break
            else:
                self.i.data = 0
        self.count += 1
        self.get_logger().info('"%f"' % self.i.data)
        self.get_logger().info('Publishing: "%d"' % self.count)

    def timer_callback(self):
        # msg = String()
        # msg.data = 'Hello World: %d' % self.i
        # if self.i.data >0:
        self.publisher_.publish(self.i)
        # self.get_logger().info('Publishing: "%d"' % self.i.data)
        # self.i += 1

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