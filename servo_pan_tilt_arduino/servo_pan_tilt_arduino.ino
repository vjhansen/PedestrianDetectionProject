#include <Servo.h>



void setup() {

servo_pan = Servo.attach(9);    // - PIN 9
servo_tilt = Servo.attach(10);  // - PIN 10

}

void loop() {
// - 0 til 180 grader
// - 1 grad pr. step
for (int pos = 0; pos <= 180; pos += 1){
  servo_pan.write(pos);
  delay(15);
}

}
