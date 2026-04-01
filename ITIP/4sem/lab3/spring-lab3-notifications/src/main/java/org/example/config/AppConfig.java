package org.example.config;

import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;

@Configuration
@ComponentScan("org.example.controller")
public class AppConfig {
    
    // @Bean
    // public EmailService emailService() {
    //     return new EmailService();
    // }

    // @Bean
    // public SmsService smsService() {
    //     return new SmsService();
    // }
    
    // @Bean
    // public NotificationManager notificationManager() {
    //     return new NotificationManager(smsService());
    // }
}
