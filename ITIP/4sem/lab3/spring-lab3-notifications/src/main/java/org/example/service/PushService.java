package org.example.service;

// import org.springframework.stereotype.Service;

// @Service
public class PushService implements MessageService {
    @Override
    public void sendMessage(String message, String recipient) {
        System.out.println("Push notification sent to " + recipient + ": " + message);
    }
    
}
