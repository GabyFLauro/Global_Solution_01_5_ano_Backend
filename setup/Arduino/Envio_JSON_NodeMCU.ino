#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <DHT.h>
#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <ArduinoJson.h>

// --- CREDENCIAIS WiFi ---
const char* ssid = "SEU_SSID";
const char* password = "SUA_SENHA";
const char* serverUrl = "http://SEU_IP:8080/api/sensor-data";

// --- MAPEAMENTO DE PINOS (NodeMCU) ---
#define DHTPIN D3              // GPIO 0 - DHT11
#define DHTTYPE DHT11

#define PIN_PRESENCA D4        // GPIO 2 - IR LM393
#define PIN_TRIG D5            // GPIO 14 - HC-SR04 Trigger
#define PIN_ECHO D6            // GPIO 12 - HC-SR04 Echo
#define PIN_POT A0             // ADC0 - Potenciômetro (Consumo Energético)
#define PIN_BUZZER D0          // GPIO 16 - Alarme (LED + Buzzer)

// --- INSTÂNCIAS DAS BIBLIOTECAS ---
DHT dht(DHTPIN, DHTTYPE);
Adafruit_MPU6050 mpu;
WiFiClient wifiClient;
HTTPClient http;

// --- VARIÁVEIS DE TEMPORIZAÇÃO ---
unsigned long tempoAnterior = 0;
const long intervaloVarredura = 2000; // Ciclo de varredura de 2 segundos

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("\n\n--- Inicializando Sistema ---");
  
  // Inicialização de Sensores e Atuadores
  dht.begin();
  
  pinMode(PIN_PRESENCA, INPUT);
  pinMode(PIN_TRIG, OUTPUT);
  pinMode(PIN_ECHO, INPUT);
  pinMode(PIN_BUZZER, OUTPUT);
  
  digitalWrite(PIN_BUZZER, LOW); // Garante alarme desligado no início

  // Inicialização do Wire para I2C (SDA=D2/GPIO4, SCL=D1/GPIO5 no NodeMCU)
  Wire.begin(D2, D1); // SDA, SCL
  delay(500);
  
  // Inicialização do MPU6050
  if (!mpu.begin(0x68)) {
    Serial.println("{\"erro\":\"Falha ao iniciar o sensor MPU6050!\"}");
  } else {
    Serial.println("MPU6050 inicializado com sucesso!");
    // Configurações ótimas para detecção de vibração estrutural
    mpu.setAccelerometerRange(MPU6050_RANGE_2_G);
    mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  }

  // Conectar ao WiFi
  conectarWiFi();
}

void loop() {
  unsigned long tempoAtual = millis();

  // Reconectar WiFi se desconectado
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi desconectado, tentando reconectar...");
    conectarWiFi();
  }

  // Executa a leitura e lógica a cada 2 segundos
  if (tempoAtual - tempoAnterior >= intervaloVarredura) {
    tempoAnterior = tempoAtual;

    // 1 e 2. LEITURA DE TEMPERATURA E UMIDADE (DHT11)
    float temperatura = dht.readTemperature();
    float umidade = dht.readHumidity();

    if (isnan(temperatura) || isnan(umidade)) {
      temperatura = 0.0;
      umidade = 0.0;
    }

    // 3. LEITURA DE VIBRAÇÃO ESTRUTURAL (MPU6050)
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);
    
    float vibracao = sqrt(pow(a.acceleration.x, 2) + pow(a.acceleration.y, 2) + pow(a.acceleration.z - 9.81, 2)) * 1.0;
    if (vibracao < 0.0) vibracao = 0.0;
    if (vibracao > 10.0) vibracao = 10.0;

    // 4. LEITURA DO CONSUMO ENERGÉTICO (Potenciômetro)
    int valorADC = analogRead(PIN_POT);
    float consumoW = (valorADC / 1023.0) * 1100.0; // NodeMCU tem 10 bits (0-1023)
    float correnteA = (consumoW / 220.0);

    // 5. LEITURA DE PRESENÇA EM ÁREA RESTRITA (IR LM393)
    int presencaRaw = digitalRead(PIN_PRESENCA);
    bool presencaInvasao = (presencaRaw == LOW);

    // 6. LEITURA DO VOLUME DE ÁGUA POTÁVEL (HC-SR04)
    digitalWrite(PIN_TRIG, LOW);
    delayMicroseconds(2);
    digitalWrite(PIN_TRIG, HIGH);
    delayMicroseconds(10);
    digitalWrite(PIN_TRIG, LOW);
    
    long duracaoEcho = pulseIn(PIN_ECHO, HIGH, 30000);
    float distanciaCm = (duracaoEcho * 0.0343) / 2.0;

    float volumeLitros = 0.0;
    if (duracaoEcho > 0 && distanciaCm >= 2.0 && distanciaCm <= 20.0) {
      volumeLitros = map(distanciaCm * 100, 2000, 20000, 10000, 0) / 100.0; // Conversão corrigida
    } else if (distanciaCm < 2.0 && duracaoEcho > 0) {
      volumeLitros = 100.0;
    } else {
      volumeLitros = 0.0;
    }

    // --- CRITÉRIOS DE ACIONAMENTO DOS ALARMES ---
    bool alarmeAtivo = false;

    if (temperatura > 40.0) alarmeAtivo = true;
    if (umidade < 20.0 || umidade > 80.0) alarmeAtivo = true;
    if (vibracao > 7.0) alarmeAtivo = true;
    if (volumeLitros < 20.0) alarmeAtivo = true;
    if (consumoW > 1000.0 || correnteA > 4.5) alarmeAtivo = true;
    if (presencaInvasao) alarmeAtivo = true;

    // Ativação do Buzzer/LED
    if (alarmeAtivo) {
      digitalWrite(PIN_BUZZER, HIGH);
    } else {
      digitalWrite(PIN_BUZZER, LOW);
    }

    // --- CRIAR JSON E ENVIAR PARA O SERVIDOR ---
    StaticJsonDocument<256> doc;
    doc["temperatura"] = round(temperatura * 10) / 10.0;
    doc["umidade"] = round(umidade * 10) / 10.0;
    doc["vibracao"] = round(vibracao * 100) / 100.0;
    doc["consumo_watts"] = round(consumoW * 10) / 10.0;
    doc["corrente_amperes"] = round(correnteA * 100) / 100.0;
    doc["presenca_invasao"] = presencaInvasao ? 1 : 0;
    doc["volume_agua"] = round(volumeLitros * 10) / 10.0;
    doc["status_alarme"] = alarmeAtivo ? 1 : 0;

    String jsonString;
    serializeJson(doc, jsonString);
    
    // Imprimir no Serial
    Serial.println(jsonString);
    
    // Enviar para o servidor
    if (WiFi.status() == WL_CONNECTED) {
      enviarDados(jsonString);
    }
  }
}

void conectarWiFi() {
  int tentativas = 0;
  Serial.print("Conectando a WiFi: ");
  Serial.println(ssid);
  
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED && tentativas < 20) {
    delay(500);
    Serial.print(".");
    tentativas++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi conectado!");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nFalha ao conectar WiFi. Continuando sem conexão...");
  }
}

void enviarDados(String jsonData) {
  if (http.begin(wifiClient, serverUrl)) {
    http.addHeader("Content-Type", "application/json");
    
    int httpCode = http.POST(jsonData);
    
    if (httpCode > 0) {
      if (httpCode == HTTP_CODE_OK) {
        Serial.println("Dados enviados com sucesso!");
      } else {
        Serial.print("Erro HTTP: ");
        Serial.println(httpCode);
      }
    } else {
      Serial.println("Falha na requisição HTTP");
    }
    
    http.end();
  } else {
    Serial.println("Falha ao conectar ao servidor");
  }
}
