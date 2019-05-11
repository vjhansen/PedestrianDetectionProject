/* 
  PDP - Styre kamerarigg med tastatur
*/

#include <Servo.h>

#define   SERVO_PAN_PIN        5
#define   SERVO_TILT_PIN       6
#define   SERVO_TILT_MAX       20       // opp
#define   SERVO_PAN_MAX        175      // venstre
#define   SERVO_MIN            0        // ned / høyre
#define   baudrate             9600

Servo servo_pan;
Servo servo_tilt;

int pos_pan = 0;
int pos_tilt = 5;
int val;
int wait_time = 15;
int pan_inc = 2;
int tilt_inc = 1;

void setup() {
  Serial.begin(baudrate);
  servo_pan.attach(SERVO_PAN_PIN);
  servo_pan.write(pos_pan);           // - skriver startposisjon for panorering
  servo_tilt.attach(SERVO_TILT_PIN);
  servo_tilt.write(pos_tilt);         // - skriver startposisjon for tilting
}

void loop() {
  if (Serial.available()) {
    val = Serial.read();
    
    if (val == 'd' && pos_pan > SERVO_MIN) {   // d = panorerer mot høyre
      pos_pan -= pan_inc;
      servo_pan.write(pos_pan);
      delay(wait_time);
    }
    
    if (val == 'a' && pos_pan < SERVO_PAN_MAX) {   // a = panorerer mot venstre
      pos_pan += pan_inc;
      servo_pan.write(pos_pan); 
      delay(wait_time);
    }
    
    if (val == 'w' && pos_tilt < SERVO_TILT_MAX) {   // w = tilter opp
      pos_tilt += tilt_inc;
      servo_tilt.write(pos_tilt);
      delay(wait_time);
    }
    
    if (val == 's' && pos_tilt > SERVO_MIN) {       // s = tilter ned
      pos_tilt -= tilt_inc;
      servo_tilt.write(pos_tilt);
      delay(wait_time);
    }
  }
}
