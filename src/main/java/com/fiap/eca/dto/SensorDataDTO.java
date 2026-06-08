package com.fiap.eca.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public class SensorDataDTO {
    
    @JsonProperty("temperatura")
    private Double temperatura;
    
    @JsonProperty("umidade")
    private Double umidade;
    
    @JsonProperty("vibracao")
    private Double vibracao;
    
    @JsonProperty(value = "consumo_watts", required = false)
    @com.fasterxml.jackson.annotation.JsonAlias("potencia")
    private Double consumoWatts;
    
    @JsonProperty(value = "corrente_amperes", required = false)
    @com.fasterxml.jackson.annotation.JsonAlias("corrente")
    private Double correnteAmperes;
    
    @JsonProperty(value = "presenca_invasao", required = false)
    @com.fasterxml.jackson.annotation.JsonAlias("presenca")
    private Integer presencaInvasao;
    
    @JsonProperty(value = "volume_agua", required = false)
    @com.fasterxml.jackson.annotation.JsonAlias("volume")
    private Double volumeAgua;
    
    @JsonProperty("status_alarme")
    private Integer statusAlarme;
    
    private Long timestamp;

    public SensorDataDTO() {
        this.timestamp = System.currentTimeMillis();
    }

    // Getters and Setters
    public Double getTemperatura() {
        return temperatura;
    }

    public void setTemperatura(Double temperatura) {
        this.temperatura = temperatura;
    }

    public Double getUmidade() {
        return umidade;
    }

    public void setUmidade(Double umidade) {
        this.umidade = umidade;
    }

    public Double getVibracao() {
        return vibracao;
    }

    public void setVibracao(Double vibracao) {
        this.vibracao = vibracao;
    }

    public Double getConsumoWatts() {
        return consumoWatts;
    }

    public void setConsumoWatts(Double consumoWatts) {
        this.consumoWatts = consumoWatts;
    }

    public Double getCorrenteAmperes() {
        return correnteAmperes;
    }

    public void setCorrenteAmperes(Double correnteAmperes) {
        this.correnteAmperes = correnteAmperes;
    }

    public Integer getPresencaInvasao() {
        return presencaInvasao;
    }

    public void setPresencaInvasao(Integer presencaInvasao) {
        this.presencaInvasao = presencaInvasao;
    }

    public Double getVolumeAgua() {
        return volumeAgua;
    }

    public void setVolumeAgua(Double volumeAgua) {
        this.volumeAgua = volumeAgua;
    }

    public Integer getStatusAlarme() {
        return statusAlarme;
    }

    public void setStatusAlarme(Integer statusAlarme) {
        this.statusAlarme = statusAlarme;
    }

    public Long getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(Long timestamp) {
        this.timestamp = timestamp;
    }
}
