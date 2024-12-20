//KODINGAN UNO -> L298N

#include <PWM.h>

// Pilih pin yang mendukung PWM (misalnya pin 10 pada Arduino Uno)
const int pwmPin = 5;
int32_t frequency = 3000; // Frekuensi dalam Hz (misalnya 20 kHz)

void setup() {
  // Inisialisasi PWM pada pin tertentu dengan frekuensi yang diinginkan
  InitTimersSafe(); // Inisialisasi timer tanpa mengganggu fungsi Arduino lainnya
  bool success = SetPinFrequencySafe(pwmPin, frequency);
  
  if (success) {
    Serial.begin(9600);
    Serial.println("PWM frequency set successfully.");
  } else {
    Serial.begin(9600);
    Serial.println("Failed to set PWM frequency.");
  }
}

void loop() {
  // Atur duty cycle PWM (misalnya 50%)
  pwmWrite(pwmPin, 128); // 128 dari 255 adalah 50%
  delay(1000);
}