package org.example.model.dto;
import java.time.LocalDateTime;

import org.example.model.enums.NotificationChannel;
import org.example.model.enums.NotificationStatus;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class NotificationDto {
    @NotBlank(message = "Заголовок не должен быть пустым")
    private String title;

    @NotBlank(message = "Текст сообщения не должен быть пустым")
    private String message;

    @NotNull(message = "Канал обязателен")
    private NotificationChannel channel;
    private NotificationStatus status;
    private LocalDateTime createdAt;
    private LocalDateTime sentAt;
    
    @NotNull(message = "Идентификатор получателя обязателен")
    private Long recipientId;
}
