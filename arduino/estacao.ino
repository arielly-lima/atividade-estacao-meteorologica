#include "DHT.h"

#define DHTPIN 2
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600); // [cite: 85]
  dht.begin();        // [cite: 86]
}

void loop() {
  float temp = dht.readTemperature(); // [cite: 89]
  float umid = dht.readHumidity();

  // Simulação caso os sensores físicos não estejam disponíveis [cite: 98]
  if (isnan(temp) || isnan(umid)) {
    temp = random(200, 320) / 10.0; // Valores aleatórios realistas [cite: 98]
    umid = random(400, 700) / 10.0;
  }

  // Envio formatado em JSON para leitura pelo script Python [cite: 78, 92, 95]
  Serial.print("{\"temperatura\":"); Serial.print(temp);
  Serial.print(",\"umidade\":"); Serial.print(umid);
  Serial.println("}");

  delay(5000); // Intervalo de 5 segundos [cite: 96]
}