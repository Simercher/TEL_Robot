import rclpy
from rclpy.node import Node

from std_msgs.msg import Float32
import sys
sys.path.append("/home/aiclub/.local/lib/python3.8/site-packages")
import serial
from witmotion import IMU

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('IMU')
        self.publisher_ = self.create_publisher(Float32, 'angle', 10)
        port = "/dev/ttyUSB0"
        baud = 921600
        self.ser = serial.Serial(port, baud, timeout=0.5)
        timer_period = 0.01  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        self.imu = IMU(port, baud)
        self.Angle = 0
    def callback(self, msg):
        print(msg)
    def timer_callback(self):
        msg = Float32()
        # msg.data = 'Hello World: %d' % self.i
        # print("Angle(deg):%10.3f %10.3f %10.3f" %int(self.imu.get_angular_velocity()[2])/100)
        self.Angle = self.imu.get_angular_velocity()[2]/100.0
        if self.Angle < 4 * -0.0006103515625 or self.Angle > 3 * 0.0006103515625:
            msg.data = self.Angle
            print(self.Angle)
            self.publisher_.publish(msg)
        # print(self.Angle)
        # self.i+=1
        # self.imu.subscribe(self.callback)
        # print(type(self.imu.get_angular_velocity()[2]))
        # self.get_logger().info('Publishing: "%s"' % msg.data)
        # self.i += 1

def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()