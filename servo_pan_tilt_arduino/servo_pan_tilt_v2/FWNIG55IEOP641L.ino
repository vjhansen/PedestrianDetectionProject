#include<Servo.h> // include server library
Servo ser; // create servo object to control a servo
int poser = 0; // initial position of server
int val; // initial value of input

void setup() {
  Serial.begin(9600); // Serial comm begin at 9600bps
  ser.attach(5);// server is connected at pin 9
}

void loop() {
  if (Serial.available()) // if serial value is available 
  {
    val = Serial.read();// then read the serial value
    if (val == 'd') //if value input is equals to d
    {
      poser += 1; //than position of servo motor increases by 1 ( anti clockwise)
      ser.write(poser);// the servo will move according to position 
      delay(15);//delay for the servo to get to the position
     }
    if (val == 'a') //if value input is equals to a
    {
      poser -= 1; //than position of servo motor decreases by 1 (clockwise)
      ser.write(poser);// the servo will move according to position 
      delay(15);//delay for the servo to get to the position
    }
  }
}
