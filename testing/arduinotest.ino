#include "Arduino.h"

int motorPin1_1 = 8;
int motorPin1_2 = 9;
int motorPin1_speed = 5;

int motorPin2_1 = 10;
int motorPin2_2 = 11;
int motorPin2_speed = 4;

void setup() {
	pinMode(motorPin1_1, OUTPUT);
	pinMode(motorPin1_2, OUTPUT);
	pinMode(motorPin1_speed, OUTPUT);

	pinMode(motorPin2_1, OUTPUT);
	pinMode(motorPin2_2, OUTPUT);
	pinMode(motorPin2_speed, OUTPUT);

	Serial.begin(9600);
	while (!Serial)
		;
	Serial.println("Speed 0 to 255");
}

int _speedAccelerate = 1;
int _speedBreak = 5;
int _speedRotate = 150;
int _speedThreshold = 110;

int _currentSpeed = 0;
bool _currentDirectionForward = true;

float _tireCircumference = 47;	// CM = 470mm
float _motorStepAngle = 1.8;	// step angle
float _distancePerStep = _tireCircumference/360*_motorStepAngle; // => 0.235 cm per step


int timer = 0;

void loop() {
	//SerialPrint("loop()");
/*
	if (false && Serial.available()) {
		int speed = Serial.parseInt();
		SerialPrint((String)speed);
		if (speed >= 0 && speed <= 255) {
			analogWrite(motorPin1_speed, speed);
			analogWrite(motorPin2_speed, speed);
		}
	} else {
		analogWrite(motorPin1_speed, 255);
		analogWrite(motorPin2_speed, 255);
	}

	analogWrite(motorPin1_1, 255);
	analogWrite(motorPin1_2, 0);
	analogWrite(motorPin2_1, 255);
	analogWrite(motorPin2_2, 0);

	delay(1000);
*/
	if(timer < 700)
		Drive();
	else if(timer < 850)
		RotateCW();
	else if(timer < 1000)
		RotateCCW();


	timer += 1;
	if(timer > 1000)
		timer = 0;
}

void Drive() {
	if(_currentSpeed < 255) {
		_currentSpeed += _speedAccelerate;
		if(_currentSpeed < _speedThreshold)
			_currentSpeed = _speedThreshold;
	}
	MoveMotor(motorPin1_1, motorPin1_2, motorPin1_speed);
	MoveMotor(motorPin2_1, motorPin2_2, motorPin2_speed);
}

void Break() {
	if(_currentSpeed > 0) {
		_currentSpeed -= _speedBreak;
		if(_currentSpeed < _speedThreshold)
			_currentSpeed = 0;
	}
	MoveMotor(motorPin1_1, motorPin1_2, motorPin1_speed);
	MoveMotor(motorPin2_1, motorPin2_2, motorPin2_speed);
}

void RotateCW() {
	Rotate(true);
}
void RotateCCW() {
	Rotate(false);
}

void Rotate(bool cw) {
	_currentSpeed = _speedRotate;
	bool storedDirection = _currentDirectionForward;

	_currentDirectionForward = cw;
	MoveMotor(motorPin1_1, motorPin1_2, motorPin1_speed);
	_currentDirectionForward = !cw;
	MoveMotor(motorPin2_1, motorPin2_2, motorPin2_speed);

	_currentDirectionForward = storedDirection;
}


bool EmergencyInterruptTriggered() {
	if(digitalRead(2) == 1)
		return true;
	return false;
}

void MoveMotor(int motorPin1, int motorPin2, int motorPinSpeed){
	int speed = _currentSpeed;
	if (speed > 0 && speed < _speedThreshold)
		speed = _speedThreshold;

	if(speed == 0) return;

	analogWrite(motorPinSpeed, speed);
	if(_currentDirectionForward) {
		analogWrite(motorPin1, 255);
		analogWrite(motorPin2, 0);
	} else {
		analogWrite(motorPin1, 0);
		analogWrite(motorPin2, 255);
	}
}



void SerialPrint(String data){
	Serial.print(data);
	Serial.println();
}


