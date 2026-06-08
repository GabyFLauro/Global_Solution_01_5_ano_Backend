import React from 'react'
import '../styles/DashboardScreen.css'
import { useSensorData } from '../../hooks/useSensorData'

export function DashboardScreen() {
  const { data, loading, error } = useSensorData()

  if (loading && !data) {
    return <div className="loading">Conectando ao servidor...</div>
  }

  if (error && !data) {
    return <div className="error">Erro: {error}</div>
  }

  if (!data) {
    return <div className="error">Aguardando dados...</div>
  }

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>🌡️ Sistema de Monitoramento ESP32</h1>
        <p className="status-text">Dashboard em Tempo Real</p>
      </header>

      {data.status_alarme === 1 && (
        <div className="alert-banner">
          🚨 ALERTA DE SEGURANÇA ATIVADO!
        </div>
      )}

      <div className="dashboard-grid">
        <SensorCard
          title="Temperatura"
          value={data.temperatura.toFixed(1)}
          unit="°C"
          threshold={40}
          isAlert={data.temperatura > 40}
        />
        <SensorCard
          title="Umidade"
          value={data.umidade.toFixed(1)}
          unit="%"
          threshold={`20-80`}
          isAlert={data.umidade < 20 || data.umidade > 80}
        />
        <SensorCard
          title="Vibração"
          value={data.vibracao.toFixed(2)}
          unit="mm/s"
          threshold={7}
          isAlert={data.vibracao > 7}
        />
        <SensorCard
          title="Consumo"
          value={data.consumo_watts.toFixed(1)}
          unit="W"
          threshold={1000}
          isAlert={data.consumo_watts > 1000}
        />
        <SensorCard
          title="Corrente"
          value={data.corrente_amperes.toFixed(2)}
          unit="A"
          threshold={4.5}
          isAlert={data.corrente_amperes > 4.5}
        />
        <SensorCard
          title="Volume"
          value={data.volume_agua.toFixed(1)}
          unit="L"
          threshold={20}
          isAlert={data.volume_agua < 20}
        />
      </div>

      <div className="alarms-section">
        <h2>🚨 Status dos Alarmes</h2>
        <div className="alarms-grid">
          <AlarmItem
            label="Temperatura"
            status={data.temperatura > 40}
            condition="T > 40°C"
          />
          <AlarmItem
            label="Umidade"
            status={data.umidade < 20 || data.umidade > 80}
            condition="U < 20% ou > 80%"
          />
          <AlarmItem
            label="Vibração"
            status={data.vibracao > 7}
            condition="V > 7.0 mm/s"
          />
          <AlarmItem
            label="Volume"
            status={data.volume_agua < 20}
            condition="Vol < 20 L"
          />
          <AlarmItem
            label="Energia"
            status={data.consumo_watts > 1000 || data.corrente_amperes > 4.5}
            condition="P > 1000W ou I > 4.5A"
          />
          <AlarmItem
            label="Presença"
            status={data.presenca_invasao === 1}
            condition="Detectada"
          />
        </div>
      </div>

      <footer className="dashboard-footer">
        <p>⏱️ Última atualização: {new Date().toLocaleTimeString('pt-BR')}</p>
        {error && <p className="error-small">{error}</p>}
      </footer>
    </div>
  )
}

interface SensorCardProps {
  title: string
  value: string
  unit: string
  threshold: number | string
  isAlert: boolean
}

function SensorCard({ title, value, unit, threshold, isAlert }: SensorCardProps) {
  return (
    <div className={`card ${isAlert ? 'alert' : 'normal'}`}>
      <div className="card-title">{title}</div>
      <div className="card-value">{value}</div>
      <div className="card-unit">{unit}</div>
      <div className={`card-status ${isAlert ? 'danger' : 'ok'}`}>
        {isAlert ? '⚠️ Alerta!' : '✓ Normal'}
      </div>
    </div>
  )
}

interface AlarmItemProps {
  label: string
  status: boolean
  condition: string
}

function AlarmItem({ label, status, condition }: AlarmItemProps) {
  return (
    <div className="alarm-item">
      <span className="alarm-label">{label}</span>
      <span className="alarm-condition">({condition})</span>
      <span className={`alarm-status ${status ? 'active' : 'ok'}`}>
        {status ? '⚠️ ALERTA' : '✓ OK'}
      </span>
    </div>
  )
}
