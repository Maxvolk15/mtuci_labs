package org.example;

import java.io.InputStream;
import java.util.Properties;
import java.util.Scanner;

import org.apache.commons.lang3.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {

    private static final Logger logger = LoggerFactory.getLogger(Main.class);

    public static void main(String[] args) {
        logger.info("Program started");

        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter a text: ");
        String input = scanner.nextLine();

        String reversed = StringUtils.reverse(input);
        logger.info("Result: {}", reversed);

        readBuildInfo();

        logger.info("Program finished");
    }

    private static void readBuildInfo() {
        try {
            InputStream input = Main.class.getClassLoader().getResourceAsStream("build-passport.properties");

            Properties prop = new Properties();
            prop.load(input);

            System.out.println("Build Info------------------");
            prop.forEach((i, j) -> System.out.println(i + ": " + j));

        } catch (Exception e) {
            logger.error("Error build-passport.properties", e);
        }
    }
}