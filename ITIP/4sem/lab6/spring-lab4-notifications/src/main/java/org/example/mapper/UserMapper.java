package org.example.mapper;

import java.time.LocalDateTime;

import org.example.model.dto.UserDto;
import org.example.model.entity.User;
import org.springframework.stereotype.Component;

@Component
public class UserMapper {
   public UserDto toDto(User user) {
        UserDto dto = new UserDto();
        dto.setName(user.getName());
        dto.setEmail(user.getEmail());
        dto.setPhone(user.getPhone());
        dto.setDeviceToken(user.getDeviceToken());
        dto.setTelegramChatId(user.getTelegramChatId());
        dto.setCreatedAt(LocalDateTime.now());
        return dto;
   }
}