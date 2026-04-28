package org.example.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;


@RestController
public class HelloController {
    @GetMapping("/hello")
    public String sayHello() {
        return "Hello, Spring!";
    }

    @GetMapping("/goodbye")
    public String sayBye() {
        return "Goodbye, Spring!";
    }

    @GetMapping("/greet")
    public String sayGreet(@RequestParam(defaultValue="Max") String name, @RequestParam(defaultValue="20") String age) {
        return "Hello, " + name + "! You are " + age + "y.o.";
    }
}