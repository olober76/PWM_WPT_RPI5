#include <avr/io.h>
#include <util/delay.h>

int main(void)
{
  // pinMode(3, OUTPUT); // Output pin for OCR2B
  pinMode(5, OUTPUT); // Output pin for OCR0B

  // Set up the 250 kHz output (but cro measures only 125 kHz)
   TCCR2A = _BV(COM2A1) | _BV(COM2B1) | _BV(WGM21) | _BV(WGM20);
   TCCR2B = _BV(WGM22) | _BV(CS20);
   OCR2A = 63;
   OCR2B = 0;

  // // Set up the 8 MHz output
  //  TCCR0A = _BV(COM0A1) | _BV(COM0B1) | _BV(WGM01) | _BV(WGM00);
  //  TCCR0B = _BV(WGM02) | _BV(CS00);
  //  OCR0A = 1;
  //  OCR0B = 0;


  // Make the 250 kHz rolling
  while (1) {
    _delay_us(5);
    if (OCR2B < 63)
      OCR2B += 5;
    else
      OCR2B = 0;
  }
}