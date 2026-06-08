import { useEffect, useState } from 'react'

interface SensorData {
  temperatura: number
  umidade: number
  vibracao: number
  consumo_watts: number
  corrente_amperes: number
  presenca_invasao: number
  volume_agua: number
  status_alarme: number
}

export function useSensorData() {
  const [data, setData] = useState<SensorData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    // Polling a cada 2 segundos
    const interval = setInterval(async () => {
      try {
        const response = await fetch('/api/sensor-data')
        if (!response.ok) throw new Error('Falha ao buscar dados')
        
        const newData = await response.json()
        setData(newData)
        setError(null)
        setLoading(false)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Erro desconhecido')
        setLoading(false)
      }
    }, 2000)

    return () => clearInterval(interval)
  }, [])

  return { data, loading, error }
}
