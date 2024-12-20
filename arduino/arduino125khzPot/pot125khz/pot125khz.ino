#include <avr/io.h>
#include <util/delay.h>

#define pot A0

void setup() {
  // Inisialisasi pin untuk PWM dan potensiometer
  pinMode(pot, INPUT); // Potentiometer input
  pinMode(5, OUTPUT);  // Output pin for OCR0B (8 MHz PWM)

  // Set up the 125 kHz output
  TCCR2A = _BV(COM2A1) | _BV(COM2B1) | _BV(WGM21) | _BV(WGM20);
  TCCR2B = _BV(WGM22) | _BV(CS20);
  OCR2A = 63;
  OCR2B = 0;


  Serial.begin(9600);
}

void loop() {
  unsigned int potVal = analogRead(pot);
  unsigned int pwmVal = map(potVal, 0, 1023, 0, 255); // Mapping to appropriate range for 8 MHz

  // Set duty cycle for 8 MHz PWM (OCR0B)
  OCR2B = pwmVal;

  Serial.println(potVal);
  _delay_us(5); // Delay to simulate the timing in the original code
}
