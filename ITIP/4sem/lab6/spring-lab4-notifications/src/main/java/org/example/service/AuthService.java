package org.example.service;
import java.time.LocalDateTime;

import org.example.model.dto.RegisterRequest;
import org.example.model.entity.User;
import org.example.model.enums.UserRole;
import org.example.repository.UserRepository;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class AuthService {
   private final UserRepository userRepository;
   private final PasswordEncoder passwordEncoder;

   public void register(RegisterRequest request) {
       checkEmailUnique(request.getEmail());
       saveUser(request, UserRole.ROLE_USER);
   }

   public void registerAdmin(RegisterRequest request) {
       checkEmailUnique(request.getEmail());
       saveUser(request, UserRole.ROLE_ADMIN);
   }

   private void checkEmailUnique(String email) {
       if (userRepository.findByEmail(email).isPresent()) {
           throw new IllegalArgumentException("Email уже используется");
       }
   }

   private void saveUser(RegisterRequest request, UserRole role) {
       User user = new User();
       user.setName(request.getName());
       user.setEmail(request.getEmail());
       user.setPassword(passwordEncoder.encode(request.getPassword()));
       user.setRole(role);
       user.setCreatedAt(LocalDateTime.now());
       userRepository.save(user);
   }
}