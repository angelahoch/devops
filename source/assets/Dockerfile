FROM eclipse-temurin:21-jdk

WORKDIR /if-demo

COPY target/*.jar if-demo-1.0.1.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "if-demo-1.0.1.jar"]