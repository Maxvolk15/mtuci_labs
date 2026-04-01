package org.example;

import org.example.config.AppConfig;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Import;


@SpringBootApplication
@Import(AppConfig.class)
public class SpringLab3NotificationsApplication {

	public static void main(String[] args) {
		SpringApplication.run(SpringLab3NotificationsApplication.class, args);
	}

}
