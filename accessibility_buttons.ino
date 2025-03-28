/*
  Button

  Turns on and off a light emitting diode(LED) connected to digital pin 13,
  when pressing a pushbutton attached to pin 2.

  The circuit:
  - LED attached from pin 13 to ground through 220 ohm resistor
  - pushbutton attached to pin 2 from +5V
  - 10K resistor attached to pin 2 from ground

  - Note: on most Arduinos there is already an LED on the board
    attached to pin 13.

  created 2005
  by DojoDave <http://www.0j0.org>
  modified 30 Aug 2011
  by Tom Igoe

  This example code is in the public domain.

  https://www.arduino.cc/en/Tutorial/BuiltInExamples/Button
*/

// constants won't change. They're used here to set pin numbers:
const int Donostiabutton = 2;  // the number of the pushbutton pin
const int Debabbutton = 3;  // the number of the pushbutton pin
const int Debagbutton = 4;  // the number of the pushbutton pin
const int Bidasoabutton = 5;  // the number of the pushbutton pin
const int Goierributton = 6;  // the number of the pushbutton pin
const int Urolakbutton = 7;  // the number of the pushbutton pin
const int Tolosabutton = 8;  // the number of the pushbutton pin
//const int ledPin = 13;    // the number of the LED pin

// variables will change:
int DonostiabuttonState = 0;  // variable for reading the pushbutton status
int DebabbuttonState = 0;  // variable for reading the pushbutton status
int DebagbuttonState = 0;  // variable for reading the pushbutton status
int BidasoabuttonState = 0;  // variable for reading the pushbutton status
int GoierributtonState = 0;  // variable for reading the pushbutton status
int UrolakbuttonState = 0;  // variable for reading the pushbutton status
int TolosabuttonState = 0;  // variable for reading the pushbutton status

int DonostiabuttonLastState = 0;  // variable for reading the pushbutton status
int DebabbuttonLastState = 0;  // variable for reading the pushbutton status
int DebagbuttonLastState = 0;  // variable for reading the pushbutton status
int BidasoabuttonLastState = 0;  // variable for reading the pushbutton status
int GoierributtonLastState = 0;  // variable for reading the pushbutton status
int UrolakbuttonLastState = 0;  // variable for reading the pushbutton status
int TolosabuttonLastState = 0;  // variable for reading the pushbutton status

void setup() {
  Serial.begin(9600);
  // initialize the LED pin as an output:
  //pinMode(ledPin, OUTPUT);
  // initialize the pushbutton pin as an input:
  pinMode(Donostiabutton, INPUT);
  pinMode(Debabbutton, INPUT);
  pinMode(Debagbutton, INPUT);
  pinMode(Bidasoabutton, INPUT);
  pinMode(Goierributton, INPUT);
  pinMode(Urolakbutton, INPUT);
  pinMode(Tolosabutton, INPUT);
}

void loop() {
  // read the state of the pushbutton value:
  DonostiabuttonState = digitalRead(Donostiabutton);
  DebabbuttonState = digitalRead(Debabbutton);
  DebagbuttonState = digitalRead(Debagbutton);
  BidasoabuttonState = digitalRead(Bidasoabutton);
  GoierributtonState = digitalRead(Goierributton);
  UrolakbuttonState = digitalRead(Urolakbutton);
  TolosabuttonState = digitalRead(Tolosabutton);

  // check if the pushbutton is pressed. If it is, the buttonState is HIGH:
  if ((DonostiabuttonState == HIGH) && (DonostiabuttonState != DonostiabuttonLastState)) {
    // turn LED on:
    //digitalWrite(ledPin, HIGH);
    Serial.write("donostia\n");
  } 
  else if ((DebabbuttonState == HIGH) && (DebabbuttonState != DebabbuttonLastState)) {
    //digitalWrite(ledPin, HIGH);
    Serial.write("debab\n");
  }
  else if ((DebagbuttonState == HIGH) && (DebagbuttonState != DebagbuttonLastState)) {
    //digitalWrite(ledPin, HIGH);
    Serial.write("debag\n");
  }
  else if ((BidasoabuttonState == HIGH) && (BidasoabuttonState != BidasoabuttonLastState)) {
    //digitalWrite(ledPin, HIGH);
    Serial.write("bidasoa\n");
  } 
  else if ((GoierributtonState == HIGH) && (GoierributtonState != GoierributtonLastState)) {
    //digitalWrite(ledPin, HIGH);
    Serial.write("goierri\n");
  }
  else if ((UrolakbuttonState == HIGH) && (UrolakbuttonState != UrolakbuttonLastState)) {
    //digitalWrite(ledPin, HIGH);
    Serial.write("urolak\n");
  }
  else if ((TolosabuttonState == HIGH) && (TolosabuttonState != TolosabuttonLastState)) {
    //digitalWrite(ledPin, HIGH);
    Serial.write("tolosa\n");
  }  
  /*
  else {
    // turn LED off:
    digitalWrite(ledPin, LOW);
  }
  */
  DonostiabuttonLastState = DonostiabuttonState;
  DebabbuttonLastState = DebabbuttonState;
  DebagbuttonLastState = DebagbuttonState;
  BidasoabuttonLastState = BidasoabuttonState;
  GoierributtonLastState = GoierributtonState;
  UrolakbuttonLastState = UrolakbuttonState;
  TolosabuttonLastState = TolosabuttonState;

}