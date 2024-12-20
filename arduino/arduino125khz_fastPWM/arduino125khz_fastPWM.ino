#include <FastPwmPin.h>

// Pin konfigurasi untuk L298N
const int enA = 3; // Enable pin A, bisa menggunakan pin PWM
const int in1 = 4; // Input pin 1
const int in2 = 7; // Input pin 2

// Pin untuk LED Built-in
const int ledPin = LED_BUILTIN; // Pin untuk LED built-in

void setup() {
  // Atur pin sebagai output
  pinMode(enA, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(ledPin, OUTPUT);

  // Inisialisasi Fast PWM pada pin 11
  FastPwmPin::enablePwmPin(11, 500000L, 50);

  // Atur arah motor
  digitalWrite(in1, HIGH); // Motor maju
  digitalWrite(in2, LOW);  // Motor maju
}

void loop() {
  // Nyalakan LED
  digitalWrite(ledPin, HIGH);
  // Kirim sinyal PWM ke motor (duty cycle 50%)
  analogWrite(enA, 128); // Nilai 128 menghasilkan duty cycle 50% pada pin PWM (0-255)
  delay(100); // Tunggu 100ms

  // Matikan LED
  digitalWrite(ledPin, LOW);
  // Matikan motor
  analogWrite(enA, 0); // Matikan sinyal PWM
  delay(100); // Tunggu 100ms
}
