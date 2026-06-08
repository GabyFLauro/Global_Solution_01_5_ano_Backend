package com.fiap.eca.controller;

import com.fiap.eca.dto.SensorDataDTO;
import org.springframework.http.ResponseEntity;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*", allowedHeaders = "*", methods = {
    RequestMethod.GET, RequestMethod.POST, RequestMethod.OPTIONS
})
public class DashboardController {

    private final SimpMessagingTemplate messagingTemplate;
    private SensorDataDTO ultimoDado;

    public DashboardController(SimpMessagingTemplate messagingTemplate) {
        this.messagingTemplate = messagingTemplate;
        this.ultimoDado = new SensorDataDTO();
    }

    /**
     * Recebe dados do ESP32 via JSON
     */
    @PostMapping("/sensor-data")
    public ResponseEntity<String> receberDadosSensor(@RequestBody SensorDataDTO sensorData) {
        this.ultimoDado = sensorData;
        messagingTemplate.convertAndSend("/topic/sensor-updates", sensorData);
        System.out.println("Dados recebidos: T=" + sensorData.getTemperatura()
                + "°C | U=" + sensorData.getUmidade()
                + "% | Alarme=" + sensorData.getStatusAlarme());
        return ResponseEntity.ok("{\"status\":\"sucesso\"}");
    }

    /**
     * Retorna os últimos dados dos sensores
     */
    @GetMapping("/sensor-data")
    public ResponseEntity<SensorDataDTO> obterUltimoDado() {
        return ResponseEntity.ok(ultimoDado);
    }
}