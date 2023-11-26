import rclpy
from rclpy.node import Node

from std_msgs.msg import Int8, Float32MultiArray, Float32, Bool
from geometry_msgs.msg import Pose2D
from sensor_msgs.msg import Joy
from math import cos, sin, sqrt, radians
import math
import numpy as np
import time
# from numba import jit, vectorize
# import numba as nb

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
        
        self.position_sub = self.create_subscription(
            Pose2D,
            'position',
            self.position_callback,
            200)
        self.position_sub

        self.imu_sub = self.create_subscription(
            Float32,
            'angle',
            self.angle_callback,
            1)
        self.imu_sub

        self.turn_shooter_sub = self.create_subscription(
            Bool,
            'turnShooter',
            self.turnShooter_callback,
            1)
        self.imu_sub

        # publisher
        self.publisher_ = self.create_publisher(Float32MultiArray, 'topic', 1)
        self.switch_bullet_pub = self.create_publisher(Bool, 'switch_bullet', 1)
        self.start_pub = self.create_publisher(Bool, 'start_bullet', 1)
        # timer_period = 0.01  # seconds
        # self.timer = self.create_timer(timer_period, self.timer_callback)
        # self.i = Int16()
        self.imu_angle = 0
        self.aoa_angle = []
        self.x = 0
        self.y = 0
        self.d = []
        self.chassisNoMove = True
        self.control_matrix = Float32MultiArray(data = [0.0, 0.0, 0.0, 0.0, 0.0])
        self.switch_bullet = Bool()
        self.start_bullet = Bool()
        self.shooter_turn_right_left = Bool()
    
    def turnShooter_callback(self, msg):
        if msg.data == True:
            pass # trun shooter to start

    def position_callback(self, msg):
        self.aoa_angle.append(msg.x - self.imu_angle)
        self.d.append(sqrt(msg.y * msg.y - 0.46 * 0.46))
        if len(self.aoa_angle) == 100 :
            # start = time.time()
            a = np.array(self.aoa_angle)
            d = np.array(self.d)
            # print(a, d)
            self.aoa_angle, self.d = self.conver(a, d)
            self.aoa_angle = self.aoa_angle.tolist()
            self.d = self.d.tolist()
            # end = time.time()
            # print(end - start)
    # @nb.njit
    def conver(self, angle, distance):
        Sum_angle = np.sum(angle)
        Sum_distance = np.sum(distance)
        avg_angle = Sum_angle / 100  # avg angle
        avg_distance = Sum_distance / 100
        s_angle = np.sum((angle - avg_angle) ** 2)
        s_distance = np.sum((distance - avg_distance)**2)
        sdAngle = np.sqrt(s_angle / 100.0)  # sd angle
        sdDistance = np.sqrt(s_distance / 100.0)
        newSumAngle = newCountAngle = newSumDistance = newCountDistance = 0

        for j in angle:
            if np.isnan(j):
                pass
            elif j < avg_angle - 1.25 * sdAngle or j > avg_angle + 1.25 * sdAngle:
                pass
            else:
                newSumAngle += j
                newCountAngle += 1
        
        for k in distance:
            if np.isnan(k):
                pass
            elif k < avg_distance - 1.25 * sdDistance or k > avg_distance + 1.25 * sdDistance:
                pass
            else:
                newSumDistance += k
                newCountDistance += 1

        # delete polar value
        newAvgAngle = newSumAngle / newCountAngle
        newAvgDistance = newSumDistance / newCountDistance

        print(newAvgAngle)
        print(newAvgDistance)
        self.y = cos(radians(newAvgAngle)) * newAvgDistance
        self.x = sin(radians(newAvgAngle)) * newAvgDistance
        self.get_logger().info('X: "%f"' % self.x)
        self.get_logger().info('Y: "%f"' % self.y)
        outliersAngle = (angle < avg_angle - 1.35 * sdAngle) | (angle > avg_angle + 1.35 * sdAngle)
        outliersDistance = (distance < avg_distance - 1.35 * sdDistance) | (distance > avg_distance + 1.35 * sdDistance)

        # print(outliers)
        angle[outliersAngle] = newAvgAngle
        distance[outliersDistance] = newAvgDistance
        
        return angle[50:], distance[50:]
    
    def angle_callback(self, msg):
        # if self.chassisNoMove == False:
        self.imu_angle += msg.data
        print(self.imu_angle)
        
    def listener_callback(self, msg):
        # for i in msg.buttons:
        #     if i:
        #         self.get_logger().info('"%s"' % i)
        # print("Buttons", msg.buttons)
        # print("Axes: ", msg.axes)
        # print("Buttom: ", msg.buttons)
        axes = msg.axes
        buttons = msg.buttons
        # calculate Mecanum wheels power
        self.control_matrix.data = output = self.calculate_mecanum(X = axes[1], Y = -axes[0], Rotate = -axes[3])
        print(output)
        for i in output:
            if i > 15 or i < -15:
                self.chassisNoMove = False
                break
        else:
            self.chassisNoMove = True
        # print(self.chassisNoMove)
        self.publisher_.publish(self.control_matrix)

        # switch bullet
        if buttons[1] == 1:
            self.switch_bullet.data = True
            self.switch_bullet_pub.publish(self.switch_bullet)
        # start
        if buttons[2] == 1:
            self.start_bullet = True
            self.start_pub.publish(self.start_bullet)

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
