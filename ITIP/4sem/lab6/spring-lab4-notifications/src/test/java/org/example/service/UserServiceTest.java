package org.example.service;
import org.example.model.dto.UserDto;
import org.example.model.entity.User;
import org.example.repository.UserRepository;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import static org.mockito.ArgumentMatchers.any;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private UserService userService;

    @Test
    void shouldCreateUser() {
        UserDto dto = UserDto.builder()
        .name("Иван Иванов")
        .email("ivan@example.com")
        .phone("+79990001122")
        .deviceToken("device-token-123")
        .telegramChatId("123456789")
        .build();
        User savedUser = new User();
        savedUser.setName(dto.getName());
        savedUser.setEmail(dto.getEmail());
        savedUser.setPhone(dto.getPhone());
        savedUser.setDeviceToken(dto.getDeviceToken());
        savedUser.setTelegramChatId(dto.getTelegramChatId());
        when(userRepository.save(any(User.class))).thenReturn(savedUser);
        User result = userService.createUser(dto);
        assertNotNull(result);
        assertEquals("Иван Иванов", result.getName());
        assertEquals("ivan@example.com", result.getEmail());
    }

    @Test
    void shouldGetUserById() {
        User user = new User();
        user.setId(15L);
        user.setName("Максос");
        user.setEmail("maxsos@example.com");
        when(userRepository.findById(15L)).thenReturn(java.util.Optional.of(user));
        User result = userService.getUserById(15L);
        assertNotNull(result);
        assertEquals("Максос", result.getName());
        assertEquals("maxsos@example.com", result.getEmail());
    }

    @Test
    void shouldDeleteUser() {
        User user = new User();
        user.setId(20L);
        when(userRepository.findById(20L)).thenReturn(java.util.Optional.of(user));
        userService.deleteUser(20L);
        verify(userRepository, times(1)).delete(any(User.class));
    }
}