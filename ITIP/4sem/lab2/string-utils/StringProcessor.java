package org.example;

public class StringProcessor {

    public static String reverse(String input) {
        return new StringBuilder(input).reverse().toString();
    }
}