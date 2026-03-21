import java.io.ByteArrayOutputStream
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter
import org.gradle.api.DefaultTask
import org.gradle.api.provider.Property
import org.gradle.api.tasks.Input
import org.gradle.api.tasks.TaskAction
import java.util.Date
import java.text.SimpleDateFormat

plugins {
    id("application")
    id("com.gradleup.shadow") version "9.4.0"
}

group = "org.example"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

dependencies {
    implementation(project(":string-utils"))

    implementation("org.apache.commons:commons-lang3:3.14.0")
    implementation("ch.qos.logback:logback-classic:1.4.14")
    implementation("org.slf4j:slf4j-api:2.0.9")

    testImplementation(platform("org.junit:junit-bom:5.9.1"))
    testImplementation("org.junit.jupiter:junit-jupiter")
}

application {
    mainClass.set("org.example.Main")
}

tasks.test {
    useJUnitPlatform()
}

tasks.shadowJar {
    manifest {
        attributes(Pair("Main-Class", "org.example.Main"))
    }
}

abstract class PrintInfoTask : DefaultTask() {
    @TaskAction
    fun print() {
        println("======================================")
        println("Это моя первая пользовательская задача!")
        println("Проект: ${project.name}")
        println("Версия Gradle: ${project.gradle.gradleVersion}")
        println("======================================")
    }
}

tasks.register<PrintInfoTask>("printInfo") {
    group = "Custom"
    description = "Выводит информацию о проекте"
}

tasks.register("generateBuildPassport") {

    val outputFile = layout.buildDirectory.file("resources/main/build-passport.properties")

    outputs.file(outputFile)

    doLast {
        val file = outputFile.get().asFile
        file.parentFile.mkdirs()

        file.writeText(
            """
            user=${System.getenv("USERNAME") ?: System.getenv("USER")}
            os=${System.getProperty("os.name")}
            java=${System.getProperty("java.version")}
            date=${SimpleDateFormat("yyyy-MM-dd-HH:mm:ss").format(Date())}
            message=Hello from Gradle!
            """.trimIndent())
    }
}

tasks.named("processResources") {
    dependsOn("generateBuildPassport")
}