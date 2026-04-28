package org.example.controller;

import org.example.service.NotificationManager;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class NotificationController {

    // private final ApplicationContext context;
    private final NotificationManager notificationManager;

    public NotificationController(NotificationManager notificationManager) {
        this.notificationManager = notificationManager;
    }

    @GetMapping("/notify")
    public String notify(@RequestParam String message, @RequestParam String email) {
        // MessageService service = new SmsService();
        // NotificationManager manager = new NotificationManager(service);
        // MessageService pushService = new PushService();
        // NotificationManager pushManager = new NotificationManager(pushService);
        // pushManager.notify("У вас сообщение", "Ivan");
        // NotificationManager manager = context.getBean(NotificationManager.class);
        // NotificationManager pushManager = new NotificationManager(context.getBean(PushService.class));
        // manager.notify(message, email);
        // pushManager.notify("У вас сообщение", "Ivan");
        notificationManager.notify(message, email);

        return "Notification send";
    }
}
