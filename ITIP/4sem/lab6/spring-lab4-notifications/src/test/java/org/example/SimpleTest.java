package org.example;
import static org.junit.jupiter.api.Assertions.assertEquals;
import org.junit.jupiter.api.Test;

public class SimpleTest {
    
    @Test
    void shouldAddNumbers() {
        int result = 2 + 3;
        assertEquals(5, result);
    }
}
