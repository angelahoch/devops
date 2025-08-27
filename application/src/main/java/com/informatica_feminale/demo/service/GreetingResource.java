package com.informatica_feminale.demo.service;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class GreetingResource {

  @GetMapping("/")
  public String hello() {
    return "Hallo liebe Kursteilnehmerinnen!";
  }

}
