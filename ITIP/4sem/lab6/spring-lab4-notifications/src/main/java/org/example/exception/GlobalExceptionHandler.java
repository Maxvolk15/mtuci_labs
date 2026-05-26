package org.example.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class GlobalExceptionHandler {

   @ExceptionHandler(BadCredentialsException.class)
   public ResponseEntity<String> handleBadCredentials(BadCredentialsException ex) {
       return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Неверный email или пароль");
   }

   @ExceptionHandler(IllegalArgumentException.class)
   public ResponseEntity<String> handleIllegalArgument(IllegalArgumentException ex) {
       return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(ex.getMessage());
   }
}