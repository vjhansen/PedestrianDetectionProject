#include <Servo.h>

//- https://github.com/embecosm/esp9-arduino-facetracker/blob/master/cam_servo.ino

#define  SERVO_PAN_MAX          180     //- max panning
#define  SERVO_TILT_MAX         50      //- max tilting (forward)
#define  HORIZONTAL_PIXELS      1920    //- screen resolution
#define  VERTICAL_PIXELS        1080    //- screen resolution
#define  SERVO_PAN_INITIAL_POS  90      //- initial pan-pos
#define  SERVO_TILT_INITIAL_POS 40      //- initial tilt-pos
#define  SERVO_PAN_PIN          5
#define  SERVO_TILT_PIN         6
#define  baudrate               9600
#define  incX 1  //- x servo rotation steps (1 deg/step)
#define  incY 1  //- y servo rotation steps

int prevX = 0; //- previous x-value
int prevY = 0; //- previous y-value

int Xval = 0;       //- store x data from serial port
int Yval = 0;       //- store y data from serial port
float SERVO_PAN_POS  = 0;
float SERVO_TILT_POS = 0;
int errorX = 10;  //- significant increments of horizontal (x) camera movement
int errorY = 10;  //- significant increments of vertical (y) camera movement

Servo SERVO_PAN;
Servo SERVO_TILT;

void setup() {
  Serial.begin(baudrate);

  SERVO_TILT.attach(SERVO_TILT_PIN);
  SERVO_PAN.attach(SERVO_PAN_PIN);

  SERVO_PAN.write(SERVO_PAN_INITIAL_POS);
  SERVO_TILT.write(SERVO_TILT_INITIAL_POS);
}

void loop () {
  while (Serial.available() > 0) {
    if (Serial.read() == 'X') {
      Xval = Serial.parseInt();
      Serial.print(Xval);
      if (Serial.read() == 'Y') {
        Yval = Serial.parseInt();
      }
    }

    //- read last servos positions
    SERVO_PAN_POS = SERVO_PAN.read();
    SERVO_TILT_POS = SERVO_TILT.read();

    if (prevX != Xval || prevY != Yval) {
      prevX = Xval;
      prevY = Yval;

      //- if X-coord is to the left from middle
      if (Xval < (HORIZONTAL_PIXELS / 2 - errorX)) {
        if (SERVO_PAN_POS >= errorX) SERVO_PAN_POS += incX; //- move to the left.
      }
      //- if X-coord is to the right from the middle
      else if (Xval > (HORIZONTAL_PIXELS / 2 + errorX)) {
        if (SERVO_PAN_POS <= SERVO_PAN_MAX - errorX) SERVO_PAN_POS -= incX; //- move to the right.
      }

      //- if Y-coord is below midscreen
      if (Yval < (VERTICAL_PIXELS / 2 - errorY)) {
        if (SERVO_TILT_POS >= 20) SERVO_TILT_POS += incY;   //- tilt down
      }

      //- if Y-coord is above midscreen
      else if (Yval > (VERTICAL_PIXELS / 2 + errorY)) {
        if (SERVO_TILT_POS <= 50) SERVO_TILT_POS -= incY;   //-  tilt up
      }
      SERVO_PAN.write(SERVO_PAN_POS);
      SERVO_TILT.write(SERVO_TILT_POS);
    }
  }
}
