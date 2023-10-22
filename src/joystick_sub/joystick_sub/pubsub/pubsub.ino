/*
 * rosserial PubSub Example
 * Prints "hello world!" and toggles led
 */

#include <ros.h>
#include <std_msgs/String.h>
#include <std_msgs/Float32MultiArray.h>

#define LIN (int []) {22, 23, 24, 25} // FL RL
#define RIN (int []) {26, 27, 28, 29} // FR RR
#define PWM (int []) {12, 13, 10, 11} // FL RL FR RR

ros::NodeHandle  nh;
//char str1[50] = "The number is "; 
int index = 0;
void messageCb( const std_msgs::Float32MultiArray& msg){
  //set FL
  if (msg.data[0] >= 0) {
    digitalWrite(LIN[0], LOW);
    digitalWrite(LIN[1], HIGH);
    analogWrite(PWM[0], msg.data[0]);
  } else {
    digitalWrite(LIN[0], HIGH);
    digitalWrite(LIN[1], LOW);
    analogWrite(PWM[0], -msg.data[0]);
  }
  //set RL
  if (msg.data[1] >= 0) {
    digitalWrite(LIN[2], LOW);
    digitalWrite(LIN[3], HIGH);
    analogWrite(PWM[1], msg.data[1]);
  } else {
    digitalWrite(LIN[2], HIGH);
    digitalWrite(LIN[3], LOW);
    analogWrite(PWM[1], -msg.data[1]);
  }
  //set FR
  if (msg.data[2] >= 0) {
    digitalWrite(RIN[0], HIGH);
    digitalWrite(RIN[1], LOW);
    analogWrite(PWM[2], msg.data[2]);
  } else {
    digitalWrite(RIN[0], LOW);
    digitalWrite(RIN[1], HIGH);
    analogWrite(PWM[2], -msg.data[2]);
  }
  //set RR
  if (msg.data[3] >= 0) {
    digitalWrite(RIN[2], HIGH);
    digitalWrite(RIN[3], LOW);
    analogWrite(PWM[3], msg.data[3]);
  } else {
    digitalWrite(RIN[2], LOW);
    digitalWrite(RIN[3], HIGH);
    analogWrite(PWM[3], -msg.data[3]);
  }
//  sprintf(str1, "%d", msg.data);
//  nh.loginfo(str1);
}

ros::Subscriber<std_msgs::Float32MultiArray> sub("topic", messageCb );

void setup()
{
  // set FL
  pinMode(LIN[0], OUTPUT);
  pinMode(LIN[1], OUTPUT);
  pinMode(PWM[0], OUTPUT);
  // set RL
  pinMode(LIN[2], OUTPUT);
  pinMode(LIN[3], OUTPUT);
  pinMode(PWM[1], OUTPUT);
  // set FR
  pinMode(RIN[0], OUTPUT);
  pinMode(RIN[1], OUTPUT);
  pinMode(PWM[2], OUTPUT);
  // set RR
  pinMode(RIN[2], OUTPUT);
  pinMode(RIN[3], OUTPUT);
  pinMode(PWM[3], OUTPUT);
  nh.initNode();
  nh.subscribe(sub);
}

void loop()
{
  nh.spinOnce();
  delay(10);
}
