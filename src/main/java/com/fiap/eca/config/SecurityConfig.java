
package com.fiap.eca.config;
 
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.web.SecurityFilterChain;
 
/**
 * Segurança completamente desabilitada.
 * Todas as requisições são permitidas sem autenticação.
 *
 * NOTA: Esta classe só é necessária se spring-boot-starter-security
 * estiver no pom.xml. Como foi removido, este arquivo pode ser deletado.
 * Mantido aqui apenas como fallback de segurança.
 */
@Configuration
@EnableWebSecurity
public class SecurityConfig {
 
    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.disable())
            .cors(cors -> cors.disable())
            .authorizeHttpRequests(auth -> auth
                .anyRequest().permitAll()
            )
            .formLogin(form -> form.disable())
            .httpBasic(httpBasic -> httpBasic.disable());
 
        return http.build();
    }
}