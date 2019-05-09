// PDP
// Styre servo-rigg med tastatur

// test om den fungerer!

#include <Servo.h>

#define   SERVO_PAN_PIN        5
#define   SERVO_TILT_PIN       6
#define   baudrate             9600

Servo servo_pan;
Servo servo_tilt;

int pos_pan = 0;
int pos_tilt = 50;
int val;
int wait_time = 15;
int pan_inc = 2;
int tilt_inc = 1;

void setup() {
  Serial.begin(baudrate);
  servo_pan.attach(SERVO_PAN_PIN);
  servo_pan.write(pos_pan);
  servo_tilt.attach(SERVO_TILT_PIN);
  servo_tilt.write(pos_tilt);
}

void loop() {
  if (Serial.available()) {
    val = Serial.read();
    
    if (val == 'd') {   // d = høyre
      pos_pan -= pan_inc;
      servo_pan.write(pos_pan);
      delay(wait_time);
    }
    
    if (val == 'a') {   // a = venstre
      pos_pan += pan_inc;
      servo_pan.write(pos_pan); 
      delay(wait_time);
    }
    
    if (val == 'w') {   // w = opp
      pos_tilt += tilt_inc;
      servo_tilt.write(pos_tilt);
      delay(wait_time);
    }
    
    if (val == 's') {   // s = ned
      pos_tilt -= tilt_inc;
      servo_tilt.write(pos_tilt);
      delay(wait_time);
    }
  }
}
