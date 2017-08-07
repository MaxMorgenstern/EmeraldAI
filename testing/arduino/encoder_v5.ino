#include <Bounce2.h>

/*
 DESCRIPTION
 ====================
 Reads the 2 switches in an encoder,
 determines direction,
 updates counter.
 No interrupts.
 Switches debounced, didn't test first, just did it anyway.
 Pushing the knob in, resuses A and B as D and E
 D is paired with A; E with B
 */


const byte ENCODER_PINA= 2;  //A&C
const byte LED_PINA= 12;
const byte LED_PIND= 10;
const byte ENCODER_PINB= 3; //B&D
const byte LED_PINB= 11;
const byte LED_PINE= 9;
const byte LED_PRESSED= 8;

const byte SWITCH_PIN= 4;

bool valueA; //debounced encoder switch reads
bool valueB;
bool notpressed;


bool motionDetected = false;
bool CW;

// not pressed
int grossCounter = 0; // total steps
int nettCounter = 0;  // cw-ccw
int fullRevolutions = 0;
int surplusSteps = 0; //part revs


// pressed; suffix P
int grossCounterP = 0; // total steps
int nettCounterP = 0;  // cw-ccw
int fullRevolutionsP = 0;
int surplusStepsP = 0; //part revs



byte cyclesPerRev =20;  //check encoder datasheet

// Instantiate 2 Bounce object
Bounce debouncerA = Bounce();
Bounce debouncerB = Bounce();
Bounce debouncerSWITCH = Bounce();

// setup ********************************************
void setup() {
  Serial.begin(9600);
  Serial.println("Setup");
  // Setup the buttons
  pinMode(ENCODER_PINA,INPUT_PULLUP);
  pinMode(ENCODER_PINB,INPUT_PULLUP);
  pinMode(SWITCH_PIN,INPUT_PULLUP);



  // After setting up the button, setup debouncer
  debouncerA.attach(ENCODER_PINA);
  debouncerA.interval(5);
  debouncerB.attach(ENCODER_PINB);
  debouncerB.interval(5);
  debouncerSWITCH.attach(SWITCH_PIN);
  debouncerSWITCH.interval(5);

  //Setup the LED
  pinMode(LED_PINA,OUTPUT);
  pinMode(LED_PINB,OUTPUT);
  pinMode(LED_PIND,OUTPUT);
  pinMode(LED_PINE,OUTPUT);
  pinMode(LED_PRESSED,OUTPUT);
  Serial.println("Setup done");
  Serial.println();
}

// loop *****************************************
void loop() {

  // Update the debouncers
  doDebounce();

  // Read the encoder switches
  doEncoderRead();

  // Update LEDs
  updateLEDs();

  //determine direction and update counter

  updateCounter();

} //loop

// my functions **************************************************
void doDebounce()
{
  debouncerA.update();
  debouncerB.update();
  debouncerSWITCH.update();
} //doDebounce

void doEncoderRead()
{
  valueA = debouncerA.read();
  valueB = debouncerB.read();
  notpressed = debouncerSWITCH.read();
  //Serial.println(notpressed);
} //doEncoderRead

void updateLEDs()
{

  if (notpressed)
  {
    digitalWrite(LED_PRESSED, LOW );
    digitalWrite(LED_PIND, LOW );
    digitalWrite(LED_PINE, LOW );

    if ( valueA) {
      digitalWrite(LED_PINA, HIGH );


    }
    else {
      digitalWrite(LED_PINA, LOW );

    }

    if ( valueB) {
      digitalWrite(LED_PINB, HIGH );

    }
    else {
      digitalWrite(LED_PINB, LOW );

    }
  } //not pressed

  if (!notpressed) //ie, pressed
  {
    digitalWrite(LED_PRESSED, HIGH );
    digitalWrite(LED_PINA, LOW );
    digitalWrite(LED_PINB, LOW );

    if ( valueA) {
      digitalWrite(LED_PIND, HIGH );


    }
    else {
      digitalWrite(LED_PIND, LOW );

    }

    if ( valueB) {
      digitalWrite(LED_PINE, HIGH );

    }
    else {
      digitalWrite(LED_PINE, LOW );

    }
  }

} //updateLEDs

void updateCounter()
{

  /*
  the possibilites are:

   AB: in a detent
   if just arrived, update counter, clear motiondetected
   otherwise do nothing
   A!B: start of CW or end of CCW
   if start, set CW bool and set motionDetected
   if at end (know becasue motionDetected already set), do nothing
   !AB: start of CCW or end of CW
   if start, clear CW bool and set motionDetected
   if at end (know becasue motionDetected already set), do nothing
   !A!B: in middle of either CW or CCW, do nothing
   */

  if (notpressed)
  {
    if (valueA && valueB && motionDetected ) //in a detent and just arrived
    {
      if (CW)
      {
        grossCounter= grossCounter + 1;
        nettCounter= nettCounter + 1; //cw +ve
      }
      else //CCW
      {
        grossCounter= grossCounter + 1;
        nettCounter= nettCounter - 1; //ccw -ve
      }
      motionDetected = false;
      Serial.print("grossCounter not pressed: ");
      Serial.println(grossCounter);
      Serial.print("nettCounter not pressed: ");
      Serial.println(nettCounter);

      fullRevolutions = nettCounter / cyclesPerRev;
      surplusSteps = nettCounter % cyclesPerRev;

      Serial.print("Nett position not pressed: ");
      Serial.print(fullRevolutions);
      Serial.print(" + ");
      Serial.println(surplusSteps);
      Serial.println(" ");




    }

    if (valueA && !valueB && !motionDetected ) // just started CW
    {
      CW= true;
      motionDetected=true;
      Serial.println("CW not pressed");

    }

    if (!valueA && valueB && !motionDetected )  //just started CCW
    {
      CW= false;
      motionDetected=true;
      Serial.println("CCW not pressed");

    }

  } // notpressed

  if (!notpressed) //ie pressed
  {
    if (valueA && valueB && motionDetected ) //in a detent and just arrived
    {
      if (CW)
      {
        grossCounterP= grossCounterP + 1;
        nettCounterP= nettCounterP + 1; //cw +ve
      }
      else //CCW
      {
        grossCounterP= grossCounterP + 1;
        nettCounterP= nettCounterP - 1; //ccw -ve
      }
      motionDetected = false;
      Serial.print("grossCounter pressed: ");
      Serial.println(grossCounterP);
      Serial.print("nettCounter pressed: ");
      Serial.println(nettCounterP);

      fullRevolutionsP = nettCounterP / cyclesPerRev;
      surplusStepsP = nettCounterP % cyclesPerRev;

      Serial.print("Nett position pressed: ");
      Serial.print(fullRevolutionsP);
      Serial.print(" + ");
      Serial.println(surplusStepsP);
      Serial.println(" ");




    }

    if (valueA && !valueB && !motionDetected ) // just started CW
    {
      CW= true;
      motionDetected=true;
      Serial.println("CW pressed");

    }

    if (!valueA && valueB && !motionDetected )  //just started CCW
    {
      CW= false;
      motionDetected=true;
      Serial.println("CCW pressed");

    }

  } // pressed

} //updateCounter


// end of sketch

