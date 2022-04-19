// Programa para modificar la intensidad de un LED
int LED = 3;                // Salida PWM a utilizar con el LED.
void setup() {
  // Bloque de código de configuración.
  pinMode(LED, OUTPUT);
}
void loop() {
  analogWrite(LED, 1);    // Enciende el LED
  delay(1000);
}
