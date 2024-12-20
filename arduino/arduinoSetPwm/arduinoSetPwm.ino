//KODINGAN UNO -> L298N

#define pot A0
#define pwm 5
int pwmVal= 0;

void setup() {
  // Inisialisasi PWM pada pin tertentu dengan frekuensi yang diinginkan
  pinMode(pot, INPUT);
  pinMode(pwm, OUTPUT);
  Serial.begin(9600);
  
}

void loop() {
  unsigned int potVal = analogRead(pot);
  pwmVal = map(potVal, 0, 1023, 0 , 255);
  Serial.println(potVal);
  analogWrite(pwm, pwmVal);
  //delay(1000);
}