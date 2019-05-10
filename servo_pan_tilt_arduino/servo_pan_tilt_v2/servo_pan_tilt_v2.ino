/*
  PDP - Skanneprogram for Arduino Uno
*/

#include <Servo.h>

#define   SERVO_PAN_PIN        5
#define   SERVO_TILT_PIN       6
#define   SERVO_PAN_INIT_POS   90
#define   SERVO_TILT_INIT_POS  5
#define   SERVO_TILT_MAX       20
#define   SERVO_PAN_MAX        180
#define   SERVO_MIN            0
#define   baudrate             9600

// - Definerer variabler
Servo SERVO_PAN;
Servo SERVO_TILT;
int time = 0;
int current_round = 0; // antall runder
int inc = 0;
int num_rounds = 0;

void setup() {
  Serial.begin(baudrate);
  SERVO_PAN.attach(SERVO_PAN_PIN);
  SERVO_TILT.attach(SERVO_TILT_PIN);
  
  SERVO_PAN.write(0); // kan disse ha verdien 0?
  SERVO_TILT.write(0);
}

void loop() {
  inc = 1;  // inkrementering
  num_rounds = 1;
  delay(5000);
  
  // - Kjører dette to ganger. Bruk funksjoner til å gi instrukser til servoer
  if(current_round <=  num_rounds) {
    up(5, 100);
    left(150, 100);
    delay(5000);
    right(30, 100);
    current_round++;
  }        
}

/*
      'up, left og right' er funksjoner for å øke posisjon til servo.
      De tar inn to variabler:
      - hvor langt servoene skal flytte seg (ex: dist_up)
      - delay, hvor fort servoene skal flytte seg (ex: delay_up, stort delay gir saktere hastighet)
*/

int left(int dist_left, int delay_left) {
  if(dist_left <= SERVO_PAN_MAX) {
    for(int pos_left = SERVO_PAN.read(); pos_left <= dist_left; pos_left = pos_left + inc) {
       SERVO_PAN.write(pos_left);
       delay(delay_left);
    }
  }
}

int right(int dist_right, int delay_right) {
  if(dist_right >= SERVO_MIN) {
    for(int pos_right = SERVO_PAN.read(); pos_right >= dist_right; pos_right = pos_right - inc) {
       SERVO_PAN.write(pos_right);
       delay(delay_right);
    }
  }
}

int up(int dist_up, int delay_up) {
  if(dist_up <= SERVO_TILT_MAX) {
    for(int pos_up = SERVO_TILT.read(); pos_up <= dist_up; pos_up = pos_up + inc) {
      SERVO_TILT.write(pos_up);
      delay(delay_up);
    }
  }
}

int down(int dist_down, int delay_down) {
  if(dist_down >= SERVO_MIN) {
    for(int pos_down = SERVO_TILT.read(); pos_down >= dist_down; pos_down = pos_down - inc) {
       SERVO_TILT.write(pos_down);
       delay(delay_down);
    }
  }
}
