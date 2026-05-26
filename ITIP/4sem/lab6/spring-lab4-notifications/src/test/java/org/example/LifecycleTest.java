package org.example;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

public class LifecycleTest {

    @BeforeEach
    void setUp() {
        System.out.println("Prepare before each test");
    }

    @AfterEach
    void tearDown() {
        System.out.println("Completion after each test");
    }

    @Test
    void firstTest() {
        System.out.println("First test");
    }

    @Test
    void secondTest() {
        System.out.println("Second test");
    }
}

