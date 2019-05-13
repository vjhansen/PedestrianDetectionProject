/*
  PDP - Områdeskanning for Arduino Uno
*/

#include <Servo.h>

#define   SERVO_PAN_PIN        5
#define   SERVO_TILT_PIN       6
#define   SERVO_PAN_INIT_POS   0
#define   SERVO_TILT_INIT_POS  5
#define   SERVO_TILT_MAX       20
#define   SERVO_PAN_MAX        175
#define   SERVO_MIN            0
#define   baudrate             9600

Servo SERVO_PAN;
Servo SERVO_TILT;

int current_round = 0;
int pan_inc = 0;
float tilt_inc = 0;
int num_rounds = 0;

void setup() {
  Serial.begin(baudrate);
  SERVO_PAN.attach(SERVO_PAN_PIN);
  SERVO_TILT.attach(SERVO_TILT_PIN);
  SERVO_PAN.write(SERVO_PAN_INIT_POS);
  SERVO_TILT.write(SERVO_TILT_INIT_POS);
}

void loop() {
  pan_inc = 2;      // - inkrementering for panorering
  tilt_inc = 0.1;   // - inkrementering for tilting
  num_rounds = 3;
  delay(1000);

  
  // - Bruk funksjoner til å gi instrukser til servoer
  while(current_round <=  num_rounds) {
    delay(1000);
    up(5, 100);
    left(150, 100);
    delay(1000);
    down(0,100);
    right(30, 100);
    current_round++;
  }        
}

/*
      'up, down, left og right' er funksjoner for å øke/redusere posisjonen til servoene.
      De tar inn to variabler:
      - hvor langt servoene skal flytte seg (ex: dist_up)
      - delay, hvor fort servoene skal flytte seg (ex: delay_up, stort delay gir saktere hastighet)
*/

int left(int dist_left, int delay_left) {
  if(dist_left <= SERVO_PAN_MAX) {
    for(int pos_left = SERVO_PAN.read(); pos_left <= dist_left; pos_left += pan_inc) {
       SERVO_PAN.write(pos_left);
       delay(delay_left);
    }
  }
}

int right(int dist_right, int delay_right) {
  if(dist_right >= SERVO_MIN) {
    for(int pos_right = SERVO_PAN.read(); pos_right >= dist_right; pos_right -= pan_inc) {
       SERVO_PAN.write(pos_right);
       delay(delay_right);
    }
  }
}

int up(int dist_up, int delay_up) {
  if(dist_up <= SERVO_TILT_MAX) {
    for(float pos_up = SERVO_TILT.read(); pos_up <= dist_up; pos_up += tilt_inc) {
      SERVO_TILT.write(pos_up);
      delay(delay_up);
    }
  }
}

int down(int dist_down, int delay_down) {
  if(dist_down >= SERVO_MIN) {
    for(float pos_down = SERVO_TILT.read(); pos_down >= dist_down; pos_down -= tilt_inc) {
       SERVO_TILT.write(pos_down);
       delay(delay_down);
    }
  }
}
