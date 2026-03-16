package com.example;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.fasterxml.jackson.databind.ObjectMapper;

public class Main {
    private static final Logger log = LoggerFactory.getLogger(Main.class);
    public static void main(String[] args) {
        try {
            Student student = new Student("Иванов Иван", "БПИ2619", 4.9f);
            log.info("Создан студент: {}, {}, {}", student.name, student.group, student.averageGrade);

            ObjectMapper mapp = new ObjectMapper();
            String jsonString = mapp.writeValueAsString(student);
            log.info("Сериализованный студент в JSON: {}", jsonString);

            Student deserializedStudent = mapp.readValue(jsonString, Student.class);
            log.info("Десериализованный студент: {}, {}, {}", deserializedStudent.name, deserializedStudent.group, deserializedStudent.averageGrade);
        } catch (Exception e) {
            log.error("Ошибка при логгировании: ", e);
        }
    }
}

class Student {
    public String name;
    public String group;
    public float averageGrade;

    public Student() {}
    public Student(String name, String group, float averageGrade) {
        this.name = name;
        this.group = group;
        this.averageGrade = averageGrade;
    }
}