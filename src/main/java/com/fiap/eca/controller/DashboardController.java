package com.fiap.eca.controller;

import com.fiap.eca.dto.SensorDataDTO;
import org.springframework.http.ResponseEntity;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*")
public class DashboardController {

    private final SimpMessagingTemplate messagingTemplate;
    private SensorDataDTO ultimoDado;

    public DashboardController(SimpMessagingTemplate messagingTemplate) {
        this.messagingTemplate = messagingTemplate;
        this.ultimoDado = new SensorDataDTO();
    }

    /**
     * Endpoint para receber dados do ESP32 via JSON
     */
    @PostMapping("/sensor-data")
    public ResponseEntity<String> receberDadosSensor(@RequestBody SensorDataDTO sensorData) {
        this.ultimoDado = sensorData;
        
        // Broadcast via WebSocket para atualizar dashboard em tempo real
        messagingTemplate.convertAndSend("/topic/sensor-updates", sensorData);
        
        System.out.println("Dados recebidos: " + sensorData.getTemperatura() + "°C");
        return ResponseEntity.ok("{\"status\":\"sucesso\"}");
    }

    /**
     * Endpoint para obter os últimos dados dos sensores
     */
    @GetMapping("/sensor-data")
    public ResponseEntity<SensorDataDTO> obterUltimoDado() {
        return ResponseEntity.ok(ultimoDado);
    }
}
