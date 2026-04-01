package org.example.service;

import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class NotificationManager {
    private final Map<String,MessageService> messageS;

    @Autowired
    public NotificationManager(Map<String, MessageService> messageServices) {
        this.messageS = messageServices;
    }
    
    public void notify(String message, String recipient) {
        MessageService service = messageS.get("customEmail");
        service.sendMessage(message, recipient);
    }

}
