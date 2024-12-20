#include <FastPwmPin.h>

#define pot A0 // Definisi pin potensiometer

void setup() {
  // Inisialisasi pin untuk PWM dan potensiometer
  pinMode(pot, INPUT); // Potentiometer input

  // Enable fast PWM on pin 11 with initial frequency 125kHz and duty cycle 50%
  FastPwmPin::enablePwmPin(11, 40000L, 50);

  Serial.begin(9600); // Mulai komunikasi serial untuk debugging
}

void loop() {
  unsigned int potVal = analogRead(pot); // Baca nilai potensiometer
  unsigned int dutyCycle = map(potVal, 0, 1023, 0, 255); // Petakan nilai potensiometer ke rentang duty cycle 0-255 (untuk FastPwmPin)

  // Set duty cycle for PWM pin 11
  // PWM duty cycle value is directly set using the analogWrite function
  analogWrite(11, dutyCycle);

  Serial.println(dutyCycle); // Cetak nilai duty cycle untuk debugging
  delay(10); // Delay singkat untuk stabilisasi

}
