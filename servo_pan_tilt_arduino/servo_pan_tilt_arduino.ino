// Siste edit: 21.02.19
// Styring av servoer


#include <Servo.h>
// se denne https://www.sparkfun.com/tutorials/304
// kan hjelpe oss med tracking.

#define PAN_PIN 3
#define TILT_PIN 2

Servo SERVO_PAN, SERVO_TILT;
int pos = 0;

void setup() {
SERVO_PAN.attach(PAN_PIN);    // - PIN 3
SERVO_TILT.attach(TILT_PIN);   // - PIN 2
  
SERVO_PAN.write(0);   //- inital pos
SERVO_TILT.write(0);
Serial.begin(9600);
}

void loop() {
  readSerial();
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
