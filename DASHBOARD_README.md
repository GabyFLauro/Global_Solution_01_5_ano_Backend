# 📊 Sistema de Monitoramento ESP32/NodeMCU - Dashboard Simples

Um dashboard em tempo real para monitoramento de sensores conectados a um NodeMCU/ESP32. Recebe dados via JSON e exibe alertas de segurança.

## 🎯 Especificações de Hardware

### Sensores Utilizados

| Sensor | Pino | Função |
|--------|------|--------|
| **DHT11** | D3 (GPIO 0) | Temperatura e Umidade |
| **MPU-6050** | D1/D2 (I2C) | Vibração / Aceleração |
| **IR LM393** | D4 (GPIO 2) | Detecção de Presença |
| **HC-SR04** | D5/D6 | Volume de Água (Ultrassom) |
| **Potenciômetro** | A0 | Simulação de Consumo Energético |
| **Alarme (LED/Buzzer)** | D0 (GPIO 16) | Alarme Sonoro e Visual |

## 🔧 Instalação e Configuração

### 1. Backend (Spring Boot)

```bash
cd /caminho/do/projeto
mvn clean install
mvn spring-boot:run
```

O servidor iniciará em `http://localhost:8080`

### 2. Arduino/NodeMCU

1. Abra o Arduino IDE
2. Instale as bibliotecas necessárias:
   - `DHT sensor library by Adafruit`
   - `Adafruit MPU6050` 
   - `Adafruit Sensor`
   - `ArduinoJson`
3. Configure as credenciais WiFi no código:
   ```cpp
   const char* ssid = "SEU_SSID";
   const char* password = "SUA_SENHA";
   const char* serverUrl = "http://SEU_IP:8080/api/sensor-data";
   ```
4. Upload do código para o NodeMCU

### 3. Dashboard

Acesse automaticamente em `http://seu_ip_servidor:8080` ou `http://localhost:8080`

## 📈 Dados Enviados

O NodeMCU envia dados em JSON a cada 2 segundos:

```json
{
  "temperatura": 28.5,
  "umidade": 65.0,
  "vibracao": 2.34,
  "consumo_watts": 450.0,
  "corrente_amperes": 2.05,
  "presenca_invasao": 0,
  "volume_agua": 85.5,
  "status_alarme": 0
}
```

## 🚨 Critérios de Alarme

O sistema ativa o pino D0 (Buzzer + LED) quando:

- **Temperatura** > 40°C (Superaquecimento)
- **Umidade** < 20% ou > 80% (Falha de Suporte de Vida)
- **Vibração** > 7.0 mm/s (Risco Estrutural)
- **Volume** < 20 Litros (Escassez Hídrica)
- **Consumo** > 1000W ou **Corrente** > 4.5A (Sobrecarga)
- **Presença** detectada (Invasão em Área Restrita)

## 🎨 Dashboard Features

✨ **Interface Responsiva** - Funciona em desktop, tablet e mobile
🔄 **Atualização em Tempo Real** - WebSocket para atualizações instantâneas
📊 **Visualização Clara** - Cards coloridos e fáceis de ler
🚨 **Alertas Visuais** - Sistema de alarme com notificações
💾 **Sem Autenticação** - Acesso livre para todos
📄 **Uma Página** - Tudo em uma única página HTML

## 📝 Estrutura do Projeto

```
src/main/
├── java/com/fiap/eca/
│   ├── controller/
│   │   ├── DashboardController.java (novo)
│   │   └── ... outros controllers
│   ├── dto/
│   │   ├── SensorDataDTO.java (novo)
│   │   └── ... outros DTOs
│   └── config/
│       └── SecurityConfig.java (modificado - sem autenticação)
└── resources/
    ├── static/
    │   └── index.html (novo - dashboard)
    └── application.properties
```

## 🔌 Endpoints API

### POST `/api/sensor-data`
Recebe dados do NodeMCU
```bash
curl -X POST http://localhost:8080/api/sensor-data \
  -H "Content-Type: application/json" \
  -d '{"temperatura":28.5,"umidade":65.0,...}'
```

### GET `/api/sensor-data`
Retorna os últimos dados recebidos
```bash
curl http://localhost:8080/api/sensor-data
```

## ⚡ Ciclo de Operação

1. NodeMCU lê sensores a cada 2 segundos
2. Dados são formatados em JSON
3. JSON é enviado via POST para o servidor
4. Dashboard recebe via WebSocket ou polling
5. Alarme é acionado se critérios forem atendidos

## 🐛 Troubleshooting

**Dashboard em branco?**
- Verifique se o servidor está rodando
- Chrome: abra DevTools (F12) para ver erros no console

**NodeMCU não se conecta ao WiFi?**
- Verifique SSID e senha
- Tente aproximar do roteador
- Reinicie o NodeMCU

**Dados não aparecem no dashboard?**
- Confirme que o NodeMCU está conectado ao WiFi
- Verifique se está enviando para o IP correto
- Tente acessar `/api/sensor-data` diretamente

## 📞 Suporte

Para dúvidas ou problemas, verifique:
1. O Serial Monitor do Arduino (115200 bps)
2. O Console do navegador (F12)
3. Logs do servidor Spring Boot

---

**Última Atualização:** 8 de junho de 2026
**Versão:** 1.0.0
