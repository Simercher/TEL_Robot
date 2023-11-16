/*
 * rosserial PubSub Example
 * Prints "hello world!" and toggles led
 */

#include <ros.h>
#include <std_msgs/String.h>
#include <std_msgs/Float32MultiArray.h>
#include <stdlib.h>

#define LIN (int []) {6, 7, 8, 9} // FL RL
#define RIN (int []) {2, 3, 4, 5} // FR RR
//#define PWM (int []) {12, 13, 10, 11} // FL RL FR RR

ros::NodeHandle  nh;
char str1[50] = ""; 
char str2[50] = "";
int index = 0;
int x[4] = {0};
void messageCb( const std_msgs::Float32MultiArray& msg){
  x[0] = (int)msg.data[0];
  x[1] = (int)msg.data[1];
  x[2] = (int)msg.data[2];
  x[3] = (int)msg.data[3];
  //set FL
  if (msg.data[0] >= 0) {
    analogWrite(LIN[1], 0);
    analogWrite(LIN[0], msg.data[0]);
  } else {
    analogWrite(LIN[1], -msg.data[0]);
    analogWrite(LIN[0], 0);
  }
  //set RL
  if (msg.data[1] >= 0) {
    analogWrite(LIN[2], 0);
    analogWrite(LIN[3], msg.data[1]);
  } else {
    analogWrite(LIN[2], -msg.data[1]);
    analogWrite(LIN[3], 0);
  }
  //set FR
  if (msg.data[2] >= 0) {
    analogWrite(RIN[0], msg.data[2]);
    analogWrite(RIN[1], 0);
  } else {
    analogWrite(RIN[0], 0);
    analogWrite(RIN[1], -msg.data[2]);
  }
  //set RR
  if (msg.data[3] >= 0) {
    analogWrite(RIN[2], msg.data[3]);
    analogWrite(RIN[3], 0);
  } else {
    analogWrite(RIN[2], 0);
    analogWrite(RIN[3], -msg.data[3]);
  }
  for (int j = 0; j < 4; j++){
    sprintf(str1, "%d", x[j]);
    strcat(str2, str1);
    strcat(str2, ",");
  }
  
//  sprintf(str1, "%d", x[1]);
//  sprintf(str1, "%d", x[2]);
//  sprintf(str1, "%d", x[1]);
  nh.loginfo(str2);
  memset(str2, 0, 50);
}

ros::Subscriber<std_msgs::Float32MultiArray> sub("topic", messageCb );

void setup()
{
  // set FL
  pinMode(LIN[0], OUTPUT);
  pinMode(LIN[1], OUTPUT);
  // set RL
  pinMode(LIN[2], OUTPUT);
  pinMode(LIN[3], OUTPUT);
  // set FR
  pinMode(RIN[0], OUTPUT);
  pinMode(RIN[1], OUTPUT);
  // set RR
  pinMode(RIN[2], OUTPUT);
  pinMode(RIN[3], OUTPUT);
  nh.initNode();
  nh.subscribe(sub);
}

void loop()
{
  nh.spinOnce();
  delay(10);
}
