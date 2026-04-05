package org.example.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Service;

@Service
public class NotificationManager {
    private final MessageService messageS;

    @Autowired
    public NotificationManager(@Qualifier("pushService") MessageService messageServices) {
        this.messageS = messageServices;
    }
    
    public void notify(String message, String recipient) {
        messageS.sendMessage(message, recipient);
    }

}
