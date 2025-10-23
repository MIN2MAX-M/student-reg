#!/bin/bash

BASE_DIR=$(pwd)

echo "Creating backend files..."

# Example backend files
cat > $BASE_DIR/people-registry-backend/src/main/java/com/example/peopleregistry/PeopleRegistryApplication.java <<EOL
package com.example.peopleregistry;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class PeopleRegistryApplication {
    public static void main(String[] args) {
        SpringApplication.run(PeopleRegistryApplication.class, args);
    }
}
EOL

cat > $BASE_DIR/people-registry-backend/src/main/resources/application.yml <<EOL
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/peopledb
    username: postgres
    password: postgres
  jpa:
    hibernate:
      ddl-auto: update
    show-sql: true
server:
  port: 8080
EOL

# Add a sample controller
cat > $BASE_DIR/people-registry-backend/src/main/java/com/example/peopleregistry/controller/PersonController.java <<EOL
package com.example.peopleregistry.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class PersonController {

    @GetMapping("/hello")
    public String hello() {
        return "Hello from People Registry!";
    }
}
EOL

echo "Creating frontend files..."

# Example frontend page
cat > $BASE_DIR/people-registry-frontend/src/pages/Home.jsx <<EOL
import React from 'react';

export default function Home() {
  return <h1>Welcome to People Registry</h1>;
}
EOL

# Example frontend service
cat > $BASE_DIR/people-registry-frontend/src/services/api.js <<EOL
import axios from 'axios';

export const api = axios.create({
  baseURL: 'http://localhost:8080',
});
EOL

echo "All files created!"

