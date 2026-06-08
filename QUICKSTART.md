# 🚀 Guia Rápido de Início - Dashboard Simples

## Início em 3 Passos

### 1️⃣ Clonar e Configurar o Backend

```bash
# Ir até o diretório do projeto
cd "/Users/gabri/Downloads/GS/Manufacturing Automation/Challenhge_ESP866_BackEND"

# Executar o servidor Spring Boot
./mvnw spring-boot:run
```

O servidor estará em: **http://localhost:8080**

### 2️⃣ Configurar o NodeMCU

**Arquivo:** `setup/Arduino/Envio_JSON_NodeMCU.ino`

Edite essas 3 linhas com seus dados:

```cpp
const char* ssid = "NOME_DO_SEU_WIFI";           // Digite seu WiFi
const char* password = "SENHA_DO_SEU_WIFI";       // Digite a senha
const char* serverUrl = "http://192.168.X.X:8080/api/sensor-data"; // IP do seu PC
```

### 3️⃣ Abrir o Dashboard

**URL:** http://localhost:8080

Pronto! 🎉 O dashboard estará recebendo dados do NodeMCU em tempo real.

---

## 🔍 Verificação Rápida

### Testar o Servidor

```bash
# Enviar um teste de dados
curl -X POST http://localhost:8080/api/sensor-data \
  -H "Content-Type: application/json" \
  -d '{
    "temperatura": 28.5,
    "umidade": 65.0,
    "vibracao": 2.5,
    "consumo_watts": 500.0,
    "corrente_amperes": 2.0,
    "presenca_invasao": 0,
    "volume_agua": 85.5,
    "status_alarme": 0
  }'
```

### Ver Últimos Dados

```bash
curl http://localhost:8080/api/sensor-data
```

---

## 📊 Dashboard Mostra

- ✅ Temperatura com status
- ✅ Umidade com status
- ✅ Vibração estrutural
- ✅ Consumo de energia
- ✅ Corrente elétrica
- ✅ Volume de água
- ✅ Alertas de segurança
- ✅ Status geral do sistema

---

## 🛑 Se der Erro

**"Servidor não responde"**
- Verifique se está rodando: `./mvnw spring-boot:run`
- Aguarde 30 segundos na primeira execução

**"Dashboard branco"**
- Abra console (F12) → Aba Console
- Procure por mensagens de erro vermelhas

**"NodeMCU não envia dados"**
- Serial Monitor: Verifique IP e WiFi
- Teste o curl acima primeiro

---

**Dúvidas?** Veja `DASHBOARD_README.md` para documentação completa.
