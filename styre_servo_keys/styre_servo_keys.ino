
// PDP
// Styre servo-rigg med tastatur

#include<Servo.h>

Servo servo_pan;
Servo servo_tilt;
int pos_pan = 0;
int pos_tilt = 50;
int val;

void setup() {
  Serial.begin(9600);
  servo_pan.attach(5);
  servo_pan.write(pos_pan);
  servo_tilt.attach(6);
  servo_tilt.write(pos_tilt);
}

void loop() {
  if (Serial.available()) {
    val = Serial.read();
    
    if (val == 'd') {   // D = høyre
      pos_pan -= 2;
      servo_pan.write(pos_pan);
      delay(15);
    }
    if (val == 'a') {   // A = venstre
      pos_pan += 2;
      servo_pan.write(pos_pan); 
      delay(15);
    }
    if (val == 'w') {   // W = opp
      pos_tilt += 1;
      servo_tilt.write(pos_tilt);
      delay(15);
    }
    if (val == 's') {   // S = ned
      pos_tilt -= 1;
      servo_tilt.write(pos_tilt);
      delay(15);
    }
  }
}
