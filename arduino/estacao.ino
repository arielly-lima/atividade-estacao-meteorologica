#include "DHT.h"
#define DHTPIN 2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600); // Frequência de comunicação [cite: 85]
  dht.begin();
}

void loop() {
  float temp = dht.readTemperature();
  float umid = dht.readHumidity();

  if (!isnan(temp) && !isnan(umid)) {
    // Formato JSON para o script Python ler facilmente [cite: 78, 92]
    Serial.print("{\"temperatura\":"); Serial.print(temp);
    Serial.print(",\"umidade\":"); Serial.print(umid);
    Serial.println("}");
  }
  delay(5000); // Leitura a cada 5 segundos [cite: 78, 96]
}