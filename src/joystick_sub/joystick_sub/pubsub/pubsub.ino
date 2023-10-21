/*
 * rosserial PubSub Example
 * Prints "hello world!" and toggles led
 */

#include <ros.h>
#include <std_msgs/String.h>
#include <std_msgs/Int16.h>

ros::NodeHandle  nh;
char str1[50] = "The number is "; 

void messageCb( const std_msgs::Int16& msg){
//  digitalWrite(13, HIGH-digitalRead(13));   // blink the led
  sprintf(str1, "%d", msg.data);
  nh.loginfo(str1);
}

ros::Subscriber<std_msgs::Int16> sub("topic", messageCb );



//std_msgs::String str_msg;
//ros::Publisher chatter("chatter", &str_msg);

//char hello[13] = "hello world!";

void setup()
{
//  pinMode(13, OUTPUT);
  nh.initNode();
//  nh.advertise(chatter);
  nh.subscribe(sub);
}

void loop()
{
//  str_msg.data = hello;
//  chatter.publish( &str_msg );
  nh.spinOnce();
  delay(10);
}
