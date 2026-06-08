# 🔗 Guia de Conexão - Sensores NodeMCU

## Mapa de Pinos NodeMCU (ESP8266)

```
       NodeMCU (ESP8266)
    ┌─────────────────────┐
    │3.3V [ ]  [ ] D0 (16)│ ← Buzzer/LED Alarme
    │GND  [ ]  [ ] D1 (5) │ ← I2C SCL (MPU)
    │    [ ]  [ ] D2 (4) │ ← I2C SDA (MPU)
    │    [ ]  [ ] D3 (0) │ ← DHT11 Data
    │    [ ]  [ ] D4 (2) │ ← IR LM393
    │    [ ]  [ ] D5 (14)│ ← HC-SR04 Trigger
    │    [ ]  [ ] D6 (12)│ ← HC-SR04 Echo
    │    [ ]  [ ] D7 (13)│
    │    [ ]  [ ] D8 (15)│
    │    [ ]  [ ] D9 (3) │
    │    [ ]  [ ] D10 (1)│
    │    [ ]  [ ] GND     │
    │    [ ]  [ ] 3.3V    │
    │VIN [ ]  [ ] A0 (ADC)│ ← Potenciômetro
    │GND [ ]  [ ] GND     │
    │    [ ]  [ ]         │
    └─────────────────────┘
```

## 1️⃣ DHT11 - Temperatura e Umidade

**Conexões:**
- VCC → 3.3V
- GND → GND
- DATA → D3 (GPIO 0)

**Esquema:**
```
DHT11
┌─────────────────┐
│1. VCC ──┐
│2. DATA ─┤─ Resistor 10kΩ ─┐
│3. (vazio)                 ├─ D3
│4. GND ──────────────────┴─ GND
└─────────────────┘
```

## 2️⃣ MPU-6050 - Vibração (I2C)

**Conexões:**
- VCC → 3.3V
- GND → GND
- SDA → D2 (GPIO 4)
- SCL → D1 (GPIO 5)

**Esquema (I2C):**
```
MPU-6050        NodeMCU
┌─────┐         ┌───┐
│VCC──┼────────→3.3V│
│GND──┼────────→GND │
│SDA──┼────────→D2  │
│SCL──┼────────→D1  │
└─────┘         └───┘
```

## 3️⃣ IR LM393 - Detecção de Presença

**Conexões:**
- VCC → 3.3V
- GND → GND
- OUT → D4 (GPIO 2)

**Esquema:**
```
IR LM393       NodeMCU
┌────────┐     ┌───┐
│VCC ───→ 3.3V │
│GND ───→ GND  │
│OUT ───→ D4   │
└────────┘     └───┘
```

## 4️⃣ HC-SR04 - Volume (Ultrassom)

**Conexões:**
- VCC → VIN (5V) *Importante: usa 5V!*
- GND → GND
- TRIG → D5 (GPIO 14)
- ECHO → D6 (GPIO 12) com **divisor de tensão** (5V → 3.3V)

**Esquema com Divisor de Tensão:**
```
HC-SR04             Divisor de Tensão       NodeMCU
┌────────┐          ┌─────────────┐
│VCC ───→ VIN (5V)  │10kΩ  4.7kΩ  │
│GND ───→ GND       │├─E──────┤   │
│TRIG ──→ D5        │├─ECHO   │   │ D6
│ECHO ──→├──10kΩ─┬──┤       └─┐
│        │       4.7kΩ        
│        │       │
│        └──GND──┴─ GND
│
ECHO (5V) ──[10kΩ]──┬─── ECHO sinal para D6 (3.3V)
                    │
              [4.7kΩ]
                    │
                   GND
```

**Por que divisor de tensão?**
- HC-SR04 saída em 5V
- NodeMCU entrada máx 3.3V
- Divisor de tensão: Vout = 5V × (4.7kΩ / (10kΩ + 4.7kΩ)) ≈ 1.55V ✓

## 5️⃣ Potenciômetro - Consumo Energético

**Conexões:**
- Terminal Lateral 1 → 3.3V
- Terminal Central → A0 (ADC)
- Terminal Lateral 2 → GND

**Esquema:**
```
Potenciômetro
┌───────┐
│ 3.3V→ ├─ Lateral 1
│   ↓   │
│ [---]───← Cursor (Terminal Central) → A0
│   ↓   │
│ GND→ ├─ Lateral 2
└───────┘
```

## 6️⃣ Alarme - LED + Buzzer

**Conexões:**
- Positivo → D0 (GPIO 16)
- Negativo → GND

**Esquema com Transistor:**
```
NodeMCU (D0)
    │
   [220Ω]
    │
    ├─→ Gate de Transistor N-channel (ex: 2N2222)
    │      ├─ Coletor ──┬──[LED]── VCC (3.3V)
    │      │            │
    │      ├─ Emissor ──┴──────────→ Buzzer →→ GND
    │
   GND ──── Base
```

---

## 🔌 Conexão Completa - Vista Geral

```
NodeMCU ESP8266
┌──────────────────────────────────────┐
│                                      │
│  D0 ─→ Alarme (Buzzer/LED)          │
│  D1 ─→ MPU-6050 SCL (I2C)           │
│  D2 ─→ MPU-6050 SDA (I2C)           │
│  D3 ─→ DHT11 Data                    │
│  D4 ─→ IR LM393 Out                  │
│  D5 ─→ HC-SR04 Trigger               │
│  D6 ─→ HC-SR04 Echo (c/ divisor)    │
│  A0 ─→ Potenciômetro Central         │
│                                      │
│  3.3V ─→ DHT11, MPU-6050, IR       │
│  VIN ─→ HC-SR04 (5V) *             │
│  GND ─→ Todos os sensores           │
└──────────────────────────────────────┘

* CRÍTICO: HC-SR04 precisa de 5V no VCC!
```

---

## ✅ Checklist de Montagem

- [ ] DHT11 conectado corretamente
- [ ] MPU-6050 I2C livre de curtos
- [ ] Resistor 10kΩ no DATA do DHT
- [ ] IR LM393 testado
- [ ] HC-SR04 com divisor de tensão (não esquecer!)
- [ ] Potenciômetro giratório
- [ ] Buzzer + LED funcionando
- [ ] Cabo USB NodeMCU conectado
- [ ] Arduino IDE com bibliotecas instaladas
- [ ] Código carregado

---

## 🔧 Solução de Problemas

### DHT11 retorna NaN
- Verifique resistor pull-up (10kΩ)
- Tente cable mais curto
- Temperatura ambiente ok?

### MPU-6050 não reconhecido
- I2C correto? (D1=SCL, D2=SDA)
- Verifique endereço I2C: `0x68`
- Cabo I2C bem conectado

### HC-SR04 sempre lê 0 ou distância errada
- **Verificar divisor de tensão!**
- ECHO conectado em D6?
- Testou pulseIn timeout (30ms)?

### Sensor não encontrado no Serial
- Velocidade serial: 115200 bps
- Cabo USB ok?
- Porta correta selecionada?

---

## 📚 Bibliotecas Necessárias (Arduino IDE)

1. DHT sensor library → Adafruit
2. Adafruit MPU6050 → Adafruit
3. Adafruit Sensor → Adafruit
4. ArduinoJson → Benoit Blanchon

```
Sketch → Include Library → Manage Libraries
→ Pesquise cada uma acima → Install
```

---

**Dúvidas?** Consulte:
- `DASHBOARD_README.md` - Documentação completa
- `QUICKSTART.md` - Início rápido
- Serial Monitor (115200 bps) - Mensagens de debug
