import rclpy
from rclpy.node import Node

from std_msgs.msg import Int8, Float32MultiArray
from sensor_msgs.msg import Joy
from math import cos, sin

F310_CODE_MAP = {
    'ABS_X': 0,
    'ABS_Y': 1,
    'ABS_Z': 2,
    'ABS_RX': 3,
    'ABS_RY': 4,
    'ABS_RZ': 5,
    'ABS_HAT0X': 6,
    'ABS_HAT0Y': 7,
    'BTN_SOUTH': 0,
    'BTN_EAST': 1,
    'BTN_NORTH': 2,
    'BTN_WEST': 3,
    'BTN_TL': 4,
    'BTN_TR': 5,
    'BTN_SELECT': 6,
    'BTN_START': 7,
    # 'BTN_MODE': 8,
    'BTN_THUMBL': 9,
    'BTN_THUMBR':10
}

class Joystick_sub(Node):

    def __init__(self):
        super().__init__('joystick_sub')
        self.subscription = self.create_subscription(
            Joy,
            'joy',
            self.listener_callback,
            1)
        self.subscription  # prevent unused variable warning
        
        # publisher
        self.publisher_ = self.create_publisher(Float32MultiArray, 'topic', 1)
        # timer_period = 0.01  # seconds
        # self.timer = self.create_timer(timer_period, self.timer_callback)
        # self.i = Int16()
        # self.count = 0
        self.control_matrix = Float32MultiArray(data = [0.0, 0.0, 0.0, 0.0, 0.0])

    def listener_callback(self, msg):
        # for i in msg.buttons:
        #     if i:
        #         self.get_logger().info('"%s"' % i)
        # print("Buttons", msg.buttons)
        print("Axes", msg.axes)
        axes = msg.axes
        # print(self.control_matrix)
        self.control_matrix.data = output = self.calculate_mecanum(X = -axes[0], Y = axes[1], Rotate = -axes[3])
        print(output)
        self.publisher_.publish(self.control_matrix)
        # for i in msg.axes:
        #     if i:
        #         # if self.count % 3 == 1:
        #         index = msg.axes.index(i)
        #         self.get_logger().info('"%d"' % index)
        #         self.i.data = 255 if round(i*255) > 255 else round(i*255)
        #         break
        #     else:
        #         # index = msg.axes.index(i)
        #         # self.get_logger().info('"%d"' % index)
        #         self.i.data = 0
        # # self.count += 1
        # self.get_logger().info('"%f"' % self.i.data)
        # self.get_logger().info('Publishing: "%d"' % self.count)

    # def timer_callback(self):
    #     # msg = String()
    #     # msg.data = 'Hello World: %d' % self.i
    #     # if self.i.data >0:
    #     self.publisher_.publish(self.i)
    #     # self.get_logger().info('Publishing: "%d"' % self.i.data)
    #     # self.i += 
    
    def calculate_mecanum(self, X=0, Y=0, Gyro=0, Rotate=0):
        control_matrix_data = self.control_matrix.data
        Y = Y*cos(Gyro) + X*sin(Gyro)
        X = X*cos(Gyro) - Y*sin(Gyro)
        deltaI = Y + X # calaulate FL RR
        deltaJ = Y - X # calaulate RL FR
        control_matrix_data[0] = deltaI + Rotate # calaulate FL
        control_matrix_data[3] = deltaI - Rotate # calaulate RR
        control_matrix_data[1] = deltaJ + Rotate # calaulate RL
        control_matrix_data[2] = deltaJ - Rotate # calaulate FR
        
        for i in range(4):
            if control_matrix_data[i] > 1:
                control_matrix_data[i] /= control_matrix_data[i]
            elif control_matrix_data[i] < -1:
                control_matrix_data[i] /= -control_matrix_data[i]
            control_matrix_data[i] = control_matrix_data[i] * 255.0
            
        # print(control_matrix_data)
        return control_matrix_data

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