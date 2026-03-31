package org.example.service;



public class NotificationManager {
    private final MessageService messageS;

    public NotificationManager(MessageService messageService) {
        this.messageS = messageService;
    }

    
    public void notify(String message, String recipient) {
        messageS.sendMessage(message, recipient);
    }
}
