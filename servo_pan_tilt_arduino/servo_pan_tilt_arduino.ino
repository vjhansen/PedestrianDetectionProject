// siste edit: 11.02.19

// Arduino-kode for styring av servoer

#include <Servo.h>
// se denne https://www.sparkfun.com/tutorials/304
// kan hjelpe oss med tracking.

Servo servo_pan, servo_tilt;
int pos = 0;

void setup() {
servo_pan.attach(3);    // - PIN 3
servo_tilt.attach(2);   // - PIN 2
}

void loop() {
// - 0 til 180 grader
// - 1 grad pr. step
  for (int pos = 0; pos <= 180; pos += 1){
    servo_pan.write(pos);
    servo_pan.write(pos);
    delay(50);
  }
  for (pos = 180; pos >= 0; pos -=1){
    servo_pan.write(pos);
    servo_tilt.write(pos);
    delay(50);
  }
}
