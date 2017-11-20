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
    Serial.print(millis());
    Serial.print("|");
    int count = 0;
    int delta = 0;
    int timeDelta = 0;
    if(id == 1)
    {
        delta = interrupt1Count - previousInterrupt1Count;
        timeDelta = millis() - previousMillis1;
        previousMillis1 = millis();
        count = interrupt1Count;
        previousInterrupt1Count = interrupt1Count;
    }
    if(id == 2)
    {
        delta = interrupt2Count - previousInterrupt2Count;
        timeDelta = millis() - previousMillis2;
        previousMillis2 = millis();
        count = interrupt2Count;
        previousInterrupt2Count = interrupt2Count;
    }
    Serial.print(count);
    Serial.print("|");
    Serial.print(delta);
    Serial.print("|");
    Serial.print(timeDelta);
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
    int timestamp = millis();
    sendData(1);
    //sendData(2);
    delay(200);
}
