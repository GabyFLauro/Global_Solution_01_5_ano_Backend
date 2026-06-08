# 🎯 Dashboard ESP32/NodeMCU

Sistema simples em uma página para monitorar sensores conectados a um NodeMCU.

## ⚡ Início Rápido

```bash
./mvnw spring-boot:run
```

Abra: **http://localhost:8080**

## 📚 Documentação

- **[COMECE_AQUI.md](COMECE_AQUI.md)** - Guia de início
- **[QUICKSTART.md](QUICKSTART.md)** - 3 passos para começar
- **[CONEXOES.md](CONEXOES.md)** - Esquemas dos sensores
- **[PINOUT_REFERENCE.md](PINOUT_REFERENCE.md)** - Pinos rápido

## 📊 Features

✅ Dashboard de uma página  
✅ Sem autenticação  
✅ Atualização em tempo real  
✅ 7 sensores monitorados  
✅ 6 alarmes de segurança  
✅ Responsivo (mobile/desktop)

## 🔧 Arquivos Principais

- `src/main/java/com/fiap/eca/Application.java` - App Spring Boot
- `src/main/java/com/fiap/eca/controller/DashboardController.java` - API
- `src/main/java/com/fiap/eca/dto/SensorDataDTO.java` - Modelo
- `src/main/resources/static/index.html` - Dashboard
- `src/main/resources/static/tester.html` - Ferramenta de teste
- `setup/Arduino/Envio_JSON_NodeMCU.ino` - Código NodeMCU

## 🔌 Sensores

| Pino | Sensor | Função |
|------|--------|--------|
| D0 | Buzzer/LED | Alarme |
| D1/D2 | MPU-6050 | Vibração (I2C) |
| D3 | DHT11 | Temp/Umidade |
| D4 | IR LM393 | Presença |
| D5/D6 | HC-SR04 | Volume (Ultrassom) |
| A0 | Potenciômetro | Energia |

## 🧪 Testar

```
http://localhost:8080/tester.html
```

## 🚀 Usar com NodeMCU

1. Edite `setup/Arduino/Envio_JSON_NodeMCU.ino` (WiFi + IP)
2. Upload no NodeMCU
3. Dashboard recebe dados automaticamente
