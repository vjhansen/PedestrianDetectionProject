// Skanneprogram
#include <Servo.h>

#define   SERVO_PAN_PIN        5
#define   SERVO_TILT_PIN       6
#define   SERVO_PAN_INIT_POS   90
#define   SERVO_TILT_INIT_POS  5
#define   SERVO_TILT_MAX       20
#define   SERVO_PAN_MAX        180
#define   SERVO_MIN            0
#define   baudrate             9600

//definerer variabler
Servo SERVO_PAN;
Servo SERVO_TILT;
int tid = 0;
int y = 0;
int i, x, j;


void setup() {
  Serial.begin(baudrate);
  SERVO_PAN.attach(SERVO_PAN_PIN);
  SERVO_TILT.attach(SERVO_TILT_PIN);
  SERVO_PAN.write(0);
  SERVO_TILT.write(0);
}

void loop() {
     x = 1;
     delay(5000);

     //kjør dette to ganger, bruk funksjoner til å gi instrukser til servoer
     if(y <=  1) {
      opp(5, 100);
      venstre(150, 100);
      delay(5000);
      hoyre(30, 100);
      y = y + 1;
     }        
}


/* -  funksjon for å øke posisjon til servo, skal samsvare med å
      vri til venstre. Tar inn to variabler, første for hvor langt
      vi skal vri, den andre for hvor fort (større verdi gir saktere
      hastighet pga delay blir større
*/

//Lager tre til bare med høyre, opp og ned, samme type input.

int venstre(int a, int b) {
  if(a <= SERVO_PAN_MAX) {
    for(int i = SERVO_PAN.read(); i <= a; i = i + 1){
       SERVO_PAN.write(i);
       delay(b);
    }
  }
}

int hoyre(int c, int d) {
  if(c >= SERVO_MIN) {
    for(i = SERVO_PAN.read(); i >= c; i = i - x){
       SERVO_PAN.write(i);
       delay(d);
    }
  }
}

int opp(int e, int f) {
  if(e <= SERVO_TILT_MAX) {
    for(j = SERVO_TILT.read(); j <= e; j = j + x){
      SERVO_TILT.write(j);
      delay(f);
    }
  }
}

int ned(int g, int h) {
  if(g >= SERVO_MIN) {
    for(j = SERVO_TILT.read(); j >= g; j = j - x){
       SERVO_TILT.write(j);
       delay(h);
    }
  }
}
