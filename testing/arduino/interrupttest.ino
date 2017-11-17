const byte ledPin = 13;
const byte interruptPin = 2;
volatile byte state = LOW;
int count = 0;
bool lock = false;

void setup() {
    pinMode(ledPin, OUTPUT);
    pinMode(interruptPin, INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(interruptPin), trigger, RISING);
    Serial.begin(230400);
}

void loop() {
    digitalWrite(ledPin, state);
    Serial.println(count);
}

void trigger() {
    state = !state;
    count++;
}
