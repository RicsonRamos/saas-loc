package com.locadora;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class LocadoraApplication {

    public static void main(String[] args) {
        java.io.File dbDir = new java.io.File("database");
        if (!dbDir.exists()) {
            dbDir.mkdirs();
        }
        
        java.io.File uploadsDir = new java.io.File("uploads");
        if (!uploadsDir.exists()) {
            uploadsDir.mkdirs();
        }

        SpringApplication.run(LocadoraApplication.class, args);
    }
}
