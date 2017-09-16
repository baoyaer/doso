package com.spider.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;  
import org.springframework.web.bind.annotation.ResponseBody;  
  
@Controller  
public class MainController {  
//    @RequestMapping("")  
//    public String index(){  
//        return "examples/index";  
//    }  
      @RequestMapping("/")  
      @ResponseBody  
      String home() {  
        return "Hello World!";  
      }  
} 