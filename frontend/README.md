# 🚀 Frontend React + TypeScript

Frontend modernon com React + TypeScript + Vite para conectar no Backend Spring Boot.

## ⚡ Início Rápido

### 1. Instalar dependências
```bash
cd frontend
npm install
```

### 2. Iniciar desenvolvimento
```bash
npm run dev
```

Acessa: **http://localhost:5173**

### 3. Build para produção
```bash
npm run build
```

## 🔌 Conecta ao Backend

O Vite proxy está configurado em `vite.config.ts`:
- `/api/*` → `http://localhost:8080/api/*`
- `/ws/*` → `ws://localhost:8080/ws/*`

**Certifique-se que o backend está rodando:**
```bash
cd ..
./mvnw spring-boot:run
```

## 📁 Estrutura

```
frontend/
├── src/
│   ├── main.tsx              (entrada)
│   ├── screens/
│   │   └── DashboardScreen/  (tela principal)
│   ├── hooks/
│   │   └── useSensorData.ts  (hook de dados)
│   └── styles/
│       └── DashboardScreen.css
├── index.html
├── vite.config.ts
├── tsconfig.json
└── package.json
```

## 🔧 Desenvolvimento

- React 18
- TypeScript
- Vite (super rápido!)
- Proxy automático para backend

## 📡 API Esperada

O backend retorna:
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

## 🚨 Alertas

Disparados automaticamente quando:
- Temperatura > 40°C
- Umidade < 20% ou > 80%
- Vibração > 7.0 mm/s
- Volume < 20L
- Energia > 1000W ou > 4.5A
- Presença detectada
