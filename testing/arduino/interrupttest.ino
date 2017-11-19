const byte interrupt1Pin = 2;
int interrupt1Count = 0;

const byte interrupt2Pin = 3;
int interrupt2Count = 0;

const int stepsPerRevelation = 20;
const int distanceInMMPerRevelation = 220;

void setup() {
    pinMode(interrupt1Pin, INPUT);
    pinMode(interrupt2Pin, INPUT);
    attachInterrupt(digitalPinToInterrupt(interrupt1Pin), countRotation1, RISING);
    attachInterrupt(digitalPinToInterrupt(interrupt2Pin), countRotation2, RISING);
    Serial.begin(230400);
}

void sendData(int id)
{
    Serial.print("Wheel");
    Serial.print("|");
    Serial.print(id);
    Serial.print("|");
    int count = 0;
    if(id == 1)
    {
        count = interrupt1Count;
    }
    if(id == 2)
    {
        count = interrupt2Count;
    }
    Serial.print(count);
    Serial.print("|");
    Serial.print(stepsPerRevelation);
    Serial.print("|");
    Serial.print(distanceInMMPerRevelation);
    Serial.print("|");
    Serial.print(distanceInMMPerRevelation/stepsPerRevelation*count);
    Serial.println("");
}

void countRotation1() {
    interrupt1Count++;
}

void countRotation2() {
    interrupt2Count++;
}

void loop() {
    sendData(1);
    sendData(2);
    delay(200);
}
