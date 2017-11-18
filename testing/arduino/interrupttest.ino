const byte interruptPin = 2;
int interruptCount = 0;
int stepsPerRevelation = 20;
int distanceInMMPerRevelation = 220;

void setup() {
    pinMode(interruptPin, INPUT);
    attachInterrupt(digitalPinToInterrupt(interruptPin), trigger, RISING);
    Serial.begin(230400);
}

void loop() {
    int wheelID = 1;
    Serial.print("Wheel");
    Serial.print("|");
    Serial.print(wheelID);
    Serial.print("|");
    Serial.print(interruptCount);
    Serial.print("|");
    Serial.print(stepsPerRevelation);
    Serial.print("|");
    Serial.print(distanceInMMPerRevelation);
    Serial.print("|");
    Serial.print(distanceInMMPerRevelation/stepsPerRevelation*interruptCount);
    Serial.println("");
    delay(200);
}

void trigger() {
    interruptCount++;
}
