#include <Servo.h>

Servo servo_pan, servo_tilt;
int data_x = 0;
int data_y = 0;
int data[1];

void setup() {
    Serial.begin(9600);
    servo_pan.attach(10);     // - PIN 9
    servo_tilt.attach(9);     // - PIN 10

    // - startpos
    servo_pan.write(90); 
    servo_tilt.write(40);
}

void loop() {
  while (Serial.available() >= 2) {
    for (int i = 0; i < 2; i++) {
      data[i] = Serial.read();
      }
      
      servo_pan.write(data[0]);
      delay(20);
      servo_tilt.write(data[1]);
      delay(20);
    
      Serial.println(data[0]);
      Serial.println(data[1]);
    }
}
