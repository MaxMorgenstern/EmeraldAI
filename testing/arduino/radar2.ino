#include "Arduino.h"
#include "Stepper.h"

// defines pins numbers
const int trigPin = 9;
const int echoPin = 10;

// defines variables
long duration;

const int stepsPerRevolution = 200;
Stepper myStepper(stepsPerRevolution, 4, 5, 6, 7);
const int enableStepper = 3;

void setup() {
    pinMode(enableStepper, OUTPUT);
    digitalWrite(enableStepper, HIGH);
    pinMode(4, OUTPUT);
    pinMode(5, OUTPUT);
    pinMode(6, OUTPUT);
    pinMode(7, OUTPUT);
    pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
    pinMode(echoPin, INPUT); // Sets the echoPin as an Input
    pinMode(irTopPin, INPUT);

    myStepper.setSpeed(180);

    Serial.begin(9600); // Starts the serial communication
}


long microsecondsToCentimeters(long microseconds){
    // The speed of sound is 340 m/s or 29 microseconds per centimeter.
    // The ping travels out and back, so to find the distance of the
    // object we take half of the distance travelled.
    return microseconds / 29 / 2;
}


void loop() {

    // DUMMY SENSOR 1
    // --------------

    // Clears the trigPin
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);

    // Sets the trigPin on HIGH state for 10 micro seconds
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    // Reads the echoPin, returns the sound wave travel time in microseconds
    duration = pulseIn(echoPin, HIGH);



    // DUMMY SENSOR 2
    // --------------

    // Clears the trigPin
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);

    // Sets the trigPin on HIGH state for 10 micro seconds
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    // Reads the echoPin, returns the sound wave travel time in microseconds
    duration = pulseIn(echoPin, HIGH);



    // Prints the distance on the Serial Monitor
    //Serial.print("Distance: ");
    //Serial.print(microsecondsToCentimeters(duration));
    //Serial.println("cm ");

    myStepper.step(1);
}
