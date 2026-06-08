#!/usr/bin/env python3
"""
Bridge Serial (ESP32) → HTTP API (Spring Boot)
Lê dados do ESP32 via Serial e envia para o backend em tempo real
Uso: python3 serial_listener.py [porta_serial] [url_servidor]
Exemplo: python3 serial_listener.py /dev/ttyUSB0 http://localhost:8080/api/sensor-data
"""

import serial
import json
import requests
import sys
import time
from datetime import datetime

# Configurações padrão
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 115200
SERVER_URL = 'http://localhost:8080/api/sensor-data'

def print_status(message, status='INFO'):
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f'[{timestamp}] [{status}] {message}')

def find_serial_ports():
    """Encontra portas seriais disponíveis"""
    import glob
    ports = []
    ports.extend(glob.glob('/dev/ttyUSB*'))
    ports.extend(glob.glob('/dev/ttyACM*'))
    ports.extend(glob.glob('/dev/cu.*'))
    for i in range(10):
        ports.append(f'COM{i}')
    return sorted(set(ports))

def convert_esp32_to_api(esp32_json):
    """Converte JSON do ESP32 para formato da API"""
    data = json.loads(esp32_json)
    
    # Mapear nomes do ESP32 para API (se necessário)
    api_data = {
        'temperatura': data.get('temperatura'),
        'umidade': data.get('umidade'),
        'vibracao': data.get('vibracao'),
        'consumo_watts': data.get('potencia'),  # ESP32 usa 'potencia'
        'corrente_amperes': data.get('corrente'),  # ESP32 usa 'corrente'
        'presenca_invasao': data.get('presenca'),  # ESP32 usa 'presenca'
        'volume_agua': data.get('volume'),  # ESP32 usa 'volume'
        'status_alarme': data.get('status_alarme')
    }
    return api_data

def main():
    global SERIAL_PORT, SERVER_URL
    
    # Processar argumentos
    if len(sys.argv) > 1:
        SERIAL_PORT = sys.argv[1]
    if len(sys.argv) > 2:
        SERVER_URL = sys.argv[2]
    
    print_status('=' * 60)
    print_status('ESP32 Serial Bridge → Dashboard API')
    print_status('=' * 60)
    print_status(f'Porta Serial: {SERIAL_PORT}')
    print_status(f'Velocidade: {BAUD_RATE} bps')
    print_status(f'URL Servidor: {SERVER_URL}')
    print_status('=' * 60)
    
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print_status(f'✓ Conectado à {SERIAL_PORT}', 'SUCCESS')
        time.sleep(2)
        
        print_status('Aguardando dados do ESP32...')
        print_status('Pressione Ctrl+C para sair')
        print_status('=' * 60)
        
        while True:
            try:
                if ser.in_waiting:
                    line = ser.readline().decode('utf-8').strip()
                    
                    if line and line.startswith('{'):
                        try:
                            # Converter dados
                            api_data = convert_esp32_to_api(line)
                            
                            # Enviar para servidor
                            try:
                                response = requests.post(
                                    SERVER_URL,
                                    json=api_data,
                                    timeout=5
                                )
                                
                                if response.status_code == 200:
                                    print_status(
                                        f'✓ T:{api_data.get("temperatura")}°C | '
                                        f'U:{api_data.get("umidade")}% | '
                                        f'V:{api_data.get("volume_agua")}L | '
                                        f'Alarme: {"🚨" if api_data.get("status_alarme") else "✓"}',
                                        'SUCCESS'
                                    )
                                else:
                                    print_status(f'Erro HTTP {response.status_code}', 'ERROR')
                            
                            except requests.exceptions.ConnectionError:
                                print_status('Não consegue conectar ao servidor', 'ERROR')
                            except requests.exceptions.Timeout:
                                print_status('Timeout ao conectar', 'ERROR')
                        
                        except json.JSONDecodeError:
                            print_status(f'JSON inválido: {line}', 'WARN')
                
                time.sleep(0.1)
            
            except KeyboardInterrupt:
                break
            except Exception as e:
                print_status(f'Erro: {e}', 'ERROR')
    
    except serial.SerialException as e:
        print_status(f'Erro na porta serial: {e}', 'ERROR')
        print_status('Portas disponíveis:')
        for port in find_serial_ports():
            print_status(f'  - {port}')
        sys.exit(1)
    
    except KeyboardInterrupt:
        pass
    
    finally:
        if ser and ser.is_open:
            ser.close()
            print_status('\nConexão fechada', 'INFO')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print_status(f'Erro fatal: {e}', 'ERROR')
        sys.exit(1)

