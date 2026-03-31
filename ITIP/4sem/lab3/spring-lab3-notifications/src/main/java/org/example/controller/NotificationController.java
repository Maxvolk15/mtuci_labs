package org.example.controller;

import org.example.service.MessageService;
import org.example.service.NotificationManager;
import org.example.service.PushService;
import org.example.service.SmsService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class NotificationController {

    @GetMapping("/notify")
    public String notify(@RequestParam String message, @RequestParam String email) {
        MessageService service = new SmsService();
        NotificationManager manager = new NotificationManager(service);
        MessageService pushService = new PushService();
        NotificationManager pushManager = new NotificationManager(pushService);
        manager.notify(message, email);
        pushManager.notify("У вас сообщение", "Ivan");

        return "Notification send (soft connect)";
    }
}
