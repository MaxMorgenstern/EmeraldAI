// Wheel encoder
const byte interrupt1Pin = 2;
int interrupt1Count = 0;
int previousInterrupt1Count = 0;

const byte interrupt2Pin = 3;
int interrupt2Count = 0;
int previousInterrupt2Count = 0;

int previousMillis1 = 0;
int previousMillis2 = 0;

const int stepsPerRevelation = 20;
const int distanceInMMPerRevelation = 220;


// Motor
const uint8_t motorPin1_1 = A3;
const uint8_t motorPin1_2 = A2;
const uint8_t motorEnablePin1 = 5;
bool motorDirectionIsForward1 = true;

const uint8_t motorPin2_1 = A5;
const uint8_t motorPin2_2 = A4;
const uint8_t motorEnablePin2 = 6;
bool motorDirectionIsForward2 = true;

uint32_t motorTimestamp;
uint32_t motorTimeout = 250;


void setup()
{
    //Wheel encoder
    pinMode(interrupt1Pin, INPUT);
    pinMode(interrupt2Pin, INPUT);
    attachInterrupt(digitalPinToInterrupt(interrupt1Pin), EncoderRotationCount1, RISING);
    attachInterrupt(digitalPinToInterrupt(interrupt2Pin), EncoderRotationCount2, RISING);


    // Motor
    pinMode(motorPin1_1, OUTPUT);
    pinMode(motorPin1_2, OUTPUT);

    pinMode(motorPin2_1, OUTPUT);
    pinMode(motorPin2_2, OUTPUT);

    //Serial.begin(230400);
    Serial.begin(115200);
}


void SendSerialDataHelper(int id)
{
    int interruptCount = 0;
    int interruptCountDelta = 0;
    int timeDelta = 0;
    if(id == 1)
    {
        interruptCountDelta = interrupt1Count - previousInterrupt1Count;
        timeDelta = millis() - previousMillis1;
        previousMillis1 = millis();
        interruptCount = interrupt1Count;
        previousInterrupt1Count = interrupt1Count;
    }
    if(id == 2)
    {
        interruptCountDelta = interrupt2Count - previousInterrupt2Count;
        timeDelta = millis() - previousMillis2;
        previousMillis2 = millis();
        interruptCount = interrupt2Count;
        previousInterrupt2Count = interrupt2Count;
    }

    Serial.print(id);
    Serial.print("|");
    Serial.print(timeDelta);
    Serial.print("|");
    Serial.print(interruptCount);
    Serial.print("|");
    Serial.print(interruptCountDelta);
}

void SendWheelData()
{
    Serial.print("Wheel");
    Serial.print("|");
    Serial.print(millis());
    Serial.print("|");
    SendSerialDataHelper(1);
    Serial.print("|");
    SendSerialDataHelper(2);
    Serial.println("");
}

void EncoderRotationCount1()
{
    if(motorDirectionIsForward1)
    {
        interrupt1Count++;
    }
    else
    {
        interrupt1Count--;
    }
}

void EncoderRotationCount2()
{
    if(motorDirectionIsForward2)
    {
        interrupt2Count++;
    }
    else
    {
        interrupt2Count--;
    }
}


void SetMotor(int id, int speed)
{
    if(id == 1)
    {
        motorDirectionIsForward1 = (speed >= 0);
        SetMotorWorker(motorPin1_1, motorPin1_2, motorEnablePin1, speed);
    }

    if(id == 2)
    {
        motorDirectionIsForward2 = (speed >= 0);
        SetMotorWorker(motorPin2_1, motorPin2_2, motorEnablePin2, speed);
    }
}

void SetMotorWorker(int pin1, int pin2, int enablePin, int speed)
{
    analogWrite(enablePin, abs(speed));

    if (speed < 0)
    {
        analogWrite(pin1, 0);
        analogWrite(pin2, 255);
    }

    if (speed > 0)
    {
        analogWrite(pin1, 255);
        analogWrite(pin2, 0);
    }

    if (speed == 0)
    {
        analogWrite(pin1, 0);
        analogWrite(pin2, 0);
    }
}

void ReadDataAndSetMotor()
{
    String data;
    if (Serial.available() > 0) {
        data = Serial.readString();

        int splitPos = data.indexOf('|');

        String serialPart1 = data.substring(0, splitPos);
        String serialPart2 = data.substring(splitPos+1);

        char buffer[10];
        serialPart1.toCharArray(buffer, 10);
        float firstValue = atof(buffer);

        serialPart2.toCharArray(buffer, 10);
        float secondValue = atof(buffer);

        SetMotor(1, firstValue);
        SetMotor(2, secondValue);

        motorTimestamp = millis();
    }
}

void CheckTimeout()
{
    if(motorTimestamp + motorTimeout < millis())
    {
        SetMotor(1, 0);
        SetMotor(2, 0);
    }
}


void loop()
{
    SendWheelData();

    ReadDataAndSetMotor();

    CheckTimeout();
}
