# 🔌 Referência Rápida de Pinos NodeMCU

## NodeMCU Pinout (ESP8266)

```
┌──────────────────────────────────────────┐
│            NodeMCU ESP8266               │
│             USB conectado abaixo         │
└──────────────────────────────────────────┘

        Lado ESQUERDO              Lado DIREITO
┌───────────────────────────┬───────────────────────────┐
│ ⚫ GND (0V)                │ ⚫ D0 (GPIO16) → 🔔 Alarme │
│ ⚫ VIN (5V entrada)        │ ⚫ D1 (GPIO5)  → 📡 I2C SCL│
│ ⚫ 3V3 (3.3V saída)        │ ⚫ D2 (GPIO4)  → 📡 I2C SDA│
│                            │ ⚫ D3 (GPIO0)  → 🌡️ DHT11  │
│                            │ ⚫ D4 (GPIO2)  → 👁️ IR     │
│                            │ ⚫ D5 (GPIO14) → 📏 TRIG   │
│ ⚫ GND (0V)                │ ⚫ D6 (GPIO12) → 📏 ECHO   │
│ ⚫ A0 (ADC - 0~3.3V)       │ ⚫ D7 (GPIO13)  (não usado) │
│                            │ ⚫ D8 (GPIO15)  (não usado) │
│ ⚫ RST (Reset)             │ ⚫ RX (UART)   (não usado) │
│ ⚫ GND (0V)                │ ⚫ TX (UART)   (não usado) │
│                            │ ⚫ GND (0V)                │
│                            │ ⚫ 3V3 (3.3V saída)        │
└───────────────────────────┴───────────────────────────┘
```

---

## Tabela de Pinos e Sensores

| Pino | GPIO | Função | Sensor | Cable |
|------|------|--------|--------|-------|
| **D0** | 16 | `OUTPUT` | 🔔 Buzzer/LED | Sinal |
| **D1** | 5 | `I2C` | 📡 MPU-6050 | **SCL** |
| **D2** | 4 | `I2C` | 📡 MPU-6050 | **SDA** |
| **D3** | 0 | `INPUT` | 🌡️ DHT11 | **DATA** |
| **D4** | 2 | `INPUT` | 👁️ IR (Presença) | **OUT** |
| **D5** | 14 | `OUTPUT` | 📏 HC-SR04 | **TRIG** |
| **D6** | 12 | `INPUT` | 📏 HC-SR04 | **ECHO** |
| **A0** | ADC | `INPUT` | ⚡ Potenciômetro | **CENTER** |
| **3.3V** | --- | `VCC` | Alimentação | **V+** |
| **VIN** | --- | `5V input` | HC-SR04 | **VCC** |
| **GND** | --- | `0V` | Terra | **GND** |

---

## Referência Código C++

```cpp
// Inicialização dos Pinos
#define DHTPIN D3              // GPIO 0  - DHT11 Data
#define PIN_PRESENCA D4        // GPIO 2  - IR LM393
#define PIN_TRIG D5            // GPIO 14 - HC-SR04 Trigger
#define PIN_ECHO D6            // GPIO 12 - HC-SR04 Echo
#define PIN_POT A0             // ADC0    - Potenciômetro
#define PIN_BUZZER D0          // GPIO 16 - Alarme

// Setup
void setup() {
  pinMode(PIN_PRESENCA, INPUT);    // Leitura
  pinMode(PIN_TRIG, OUTPUT);       // Envio pulso
  pinMode(PIN_ECHO, INPUT);        // Recebe pulso
  pinMode(PIN_BUZZER, OUTPUT);     // Liga/desliga
  
  Wire.begin(D2, D1);  // SDA, SCL para I2C/MPU
}

// Loop - Leitura
void loop() {
  int valor = digitalRead(PIN_PRESENCA);  // Lê presença
  int distancia = pulseIn(PIN_ECHO, HIGH);// Lê eco
  int adc = analogRead(PIN_POT);          // Lê potenciômetro (0-1023)
  
  // Ativa alarme
  digitalWrite(PIN_BUZZER, HIGH);  // Liga
  digitalWrite(PIN_BUZZER, LOW);   // Desliga
}
```

---

## Rápida Referência: Leitura de Dados

### Digital (0 ou 1)
```cpp
int valor = digitalRead(PIN_PRESENCA);  // Lê presença → 0 ou 1
```

### Analógico (0-1023)
```cpp
int valor = analogRead(PIN_POT);        // Lê potenciômetro → 0 a 1023
float tensao = valor * (3.3 / 1023.0);  // Converte para volts
```

### I2C (Wire)
```cpp
Wire.begin(D2, D1);  // SDA em D2, SCL em D1
mpu.begin();         // Inicializa sensor
mpu.getEvent(&a);    // Lê aceleração
```

### Distância (HC-SR04)
```cpp
digitalWrite(PIN_TRIG, LOW);   delayMicroseconds(2);
digitalWrite(PIN_TRIG, HIGH);  delayMicroseconds(10);
digitalWrite(PIN_TRIG, LOW);
long tempo = pulseIn(PIN_ECHO, HIGH, 30000);
float distancia = (tempo * 0.0343) / 2.0;  // em cm
```

---

## Verificação de Conexão Serial

```
Serial.begin(115200);  // Velocidade do NodeMCU
while (!Serial);       // Aguarda conexão
Serial.println("Conectado!");

// Monitor Serial: Ctrl+Shift+M (Arduino IDE)
// Velocidade: 115200 bps ⚠️ CRÍTICO!
```

---

## Conversão de Valores

### Temperatura (DHT11)
```cpp
float temp = dht.readTemperature();  // °C
// Limite de alarme: > 40°C
```

### Umidade (DHT11)
```cpp
float umidade = dht.readHumidity();  // %
// Limite de alarme: < 20% ou > 80%
```

### Vibração (MPU-6050)
```cpp
float vibracao = sqrt(ax² + ay² + az²);  // m/s²
// Converter para mm/s: multiply by 1000
// Limite de alarme: > 7.0 mm/s
```

### Energia (Potenciômetro)
```cpp
int adc = analogRead(PIN_POT);          // 0-1023
float watts = (adc / 1023.0) * 1100.0;  // 0-1100W
// Limite de alarme: > 1000W
```

### Volume Água (HC-SR04)
```cpp
float distancia = (tempo * 0.0343) / 2.0;  // cm
float volume = map(distancia, 20, 2, 0, 100); // Litros
// Limite de alarme: < 20L
```

---

## 🔗 Mapeamento Direto Código ↔ Hardware

```
Código Arduino        →    Pino Físico    →    Sensor
====================================================

D0 (GPIO 16)          →    Pino D0        →    🔔 Buzzer
D1 (GPIO 5)           →    Pino D1        →    📡 MPU-6050 SCL
D2 (GPIO 4)           →    Pino D2        →    📡 MPU-6050 SDA
D3 (GPIO 0)           →    Pino D3        →    🌡️  DHT11 Data
D4 (GPIO 2)           →    Pino D4        →    👁️  IR
D5 (GPIO 14)          →    Pino D5        →    📏 HC-SR04 Trig
D6 (GPIO 12)          →    Pino D6        →    📏 HC-SR04 Echo
A0 (ADC)              →    Pino A0        →    ⚡ Potenciômetro
3.3V                  →    3.3V           →    VCC Sensores
VIN                   →    VIN (5V input) →    VCC HC-SR04
GND                   →    GND            →    Terra
```

---

## ⚡ Voltagens

| Pino | Saída | Entrada Máx | Uso |
|------|-------|-------------|-----|
| **3.3V** | 3.3V | --- | Alimentação sensores |
| **VIN** | 5V input | --- | HC-SR04 VCC |
| **D0-D8** | 3.3V | 3.3V | GPIO digitais |
| **A0** | --- | 3.3V | Entrada analógica |

⚠️ **IMPORTANTE:** 
- HC-SR04 ECHO precisa de divisor de tensão (5V → 3.3V)
- Não conecte 5V diretamente nos pinos GPIO

---

## 🧪 Teste Rápido da Porta Serial

```bash
# Mac/Linux
screen /dev/ttyUSB0 115200
# Ctrl+A, depois Ctrl+\ para sair

# Windows (Git Bash)
screen COM3 115200

# Python
python3 serial_listener.py /dev/ttyUSB0
```

---

## Sumário Visual

```
     ┌─────────────┐
     │   NodeMCU   │
     │  ESP8266    │
     └─────────────┘
          │
    ┌─────┼─────┬─────┬─────┬─────┐
    │     │     │     │     │     │
   3.3V  GND   D0   D1   D2   D3
    │     │     │     │     │     │
    ├─ 🌡️  ├─ 🔔 ├─ 📡 ├─ 📡 └─ 🌡️
    ┊
    │
   D4    D5    D6    A0   VIN
    │     │     │     │     │
    ├─ 👁️ ├─ 📏 ├─ 📏 ├─ ⚡ ├─ 📏
    │ (IR) │(TRIG)(ECHO)(POT)(+5V)
```

---

**Guia Rápido v1.0**  
**Imprime e cola na sua mesa! 📌**

