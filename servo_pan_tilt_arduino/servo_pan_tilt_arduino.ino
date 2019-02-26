// 26.feb
// https://www.instructables.com/id/FACE-TRACKING-USING-ARDUINO-/

#include <Servo.h>

Servo servo_pan, servo_tilt;
int x, prevX, y, prevY;

void setup() {
  Serial.begin(9600);
  servo_pan.attach(10);
  servo_tilt.attach(9);
  servo_pan.write(90);
  servo_tilt.write(40);
}

void loop() {
  if (Serial.available() > 0) 
  {
    if (Serial.read() == 'X') 
    {
      x = parseInt();
      Serial.println(x);
      if (Serial.read() == 'Y') 
      {
        y = parseInt();
        Serial.println(y);
        moveCam();
      }
     }
     while(Serial.available() > 0) 
     {
        Serial.read();
     }
    }
 }

 void moveCam() {
  if (prevX != x || prevY != y)
  {
    prevX = x;
    prevY = y;

    // map(value, fromLow, fromHigh, toLow, toHigh)
    // https://www.arduino.cc/reference/en/language/functions/math/map/
    
      // må teste her, setter min/max verdier for servoene
      int servoX = map(x, 600, 0, 70, 179);
      int servoY = map(y, 450, 0, 179, 95);
    
    servoX = min(servoX, 179);
    servoX = max(servoX, 70);
    servoY = min(servoY, 180);
    servoY = max(servoY, 95);
    servo_pan.write(servoX);
    servo_tilt.write(servoY);
  }
}
