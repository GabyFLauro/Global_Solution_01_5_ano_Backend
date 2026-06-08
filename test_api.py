#!/usr/bin/env python3
"""
Script de teste da API do Dashboard
Verifica se o servidor está respondendo corretamente
"""

import requests
import json
import sys
from datetime import datetime

RESET = '\033[0m'
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'

def print_header():
    print(f"\n{BLUE}{'='*60}")
    print('  Teste de Conectividade - Dashboard Sensores')
    print(f"{'='*60}{RESET}\n")

def print_success(message):
    print(f"{GREEN}✓ {message}{RESET}")

def print_error(message):
    print(f"{RED}✗ {message}{RESET}")

def print_warning(message):
    print(f"{YELLOW}⚠ {message}{RESET}")

def test_server(url):
    """Testa se o servidor está respondendo"""
    print(f"Testando servidor: {BLUE}{url}{RESET}")
    
    try:
        response = requests.get(url, timeout=5)
        print_success("Servidor respondendo")
        return True
    except requests.exceptions.ConnectionError:
        print_error("Não consegue conectar ao servidor")
        return False
    except requests.exceptions.Timeout:
        print_error("Timeout - servidor demorando muito")
        return False
    except Exception as e:
        print_error(f"Erro: {e}")
        return False

def test_api_get(url):
    """Testa GET /api/sensor-data"""
    print("\nTestando GET /api/sensor-data...")
    
    try:
        response = requests.get(f"{url}/api/sensor-data", timeout=5)
        print_success(f"Resposta: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"  Temperatura: {data.get('temperatura', 'N/A')}°C")
            print(f"  Umidade: {data.get('umidade', 'N/A')}%")
            print(f"  Volume: {data.get('volume_agua', 'N/A')}L")
            print(f"  Alarme: {'🚨 ATIVO' if data.get('status_alarme') else '✓ OK'}")
        else:
            print_warning("Status inesperado")
        
        return True
    except Exception as e:
        print_error(f"Erro na requisição: {e}")
        return False

def test_api_post(url):
    """Testa POST /api/sensor-data com dados de exemplo"""
    print("\nTestando POST /api/sensor-data...")
    
    dados = {
        "temperatura": 28.5,
        "umidade": 65.0,
        "vibracao": 2.5,
        "consumo_watts": 500.0,
        "corrente_amperes": 2.2,
        "presenca_invasao": 0,
        "volume_agua": 85.5,
        "status_alarme": 0
    }
    
    print("Enviando JSON teste:")
    print(json.dumps(dados, indent=2))
    
    try:
        response = requests.post(
            f"{url}/api/sensor-data",
            json=dados,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        print_success(f"Resposta: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"  Servidor respondeu: {result}")
        else:
            print_warning(f"Resposta: {response.text}")
        
        return response.status_code == 200
    except Exception as e:
        print_error(f"Erro ao enviar dados: {e}")
        return False

def test_dashboard(url):
    """Testa acesso ao dashboard HTML"""
    print("\nTestando Dashboard (GET /)...")
    
    try:
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            if 'html' in response.text.lower() or 'dashboard' in response.text.lower():
                print_success("Dashboard carregando")
                return True
            else:
                print_warning("Página não parece ser o dashboard")
                return False
        else:
            print_error(f"Status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Erro ao acessar dashboard: {e}")
        return False

def main():
    print_header()
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = "http://localhost:8080"
    
    print(f"URL Base: {BLUE}{url}{RESET}\n")
    
    # Testes
    tests = []
    
    tests.append(("Servidor", test_server(url)))
    tests.append(("Dashboard", test_dashboard(url)))
    tests.append(("GET API", test_api_get(url)))
    tests.append(("POST API", test_api_post(url)))
    
    # Resumo
    print(f"\n{BLUE}{'='*60}")
    print("  Resumo dos Testes")
    print(f"{'='*60}{RESET}")
    
    passed = sum(1 for _, result in tests if result)
    total = len(tests)
    
    for name, result in tests:
        symbol = "✓" if result else "✗"
        color = GREEN if result else RED
        print(f"{color}{symbol}{RESET} {name}")
    
    print(f"\n{BLUE}Resultado: {passed}/{total} testes passaram{RESET}\n")
    
    if passed == total:
        print_success("Todos os testes passaram! Sistema pronto.")
        return 0
    else:
        print_error("Alguns testes falharam. Verifique as configurações.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
