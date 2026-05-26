package org.example.service;
import java.util.Optional;

import org.example.model.dto.NotificationDto;
import org.example.model.enums.NotificationChannel;
import org.example.repository.NotificationRepository;
import org.example.repository.UserRepository;
import static org.junit.jupiter.api.Assertions.assertThrows;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import static org.mockito.Mockito.when;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class NotificationServiceExceptionTest {

    @Mock
    private NotificationRepository notificationRepository;

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private NotificationService notificationService;

    @Test
    void shouldThrowExceptionWhenUserNotFound() {

        NotificationDto dto = NotificationDto.builder()
            .title("Напоминание")
            .message("Сообщение")
            .channel(NotificationChannel.EMAIL)
            .recipientId(99L)
            .build();

        when(userRepository.findById(99L)).thenReturn(Optional.empty());

        assertThrows(RuntimeException.class, () -> notificationService.createNotification(dto));
    }
}