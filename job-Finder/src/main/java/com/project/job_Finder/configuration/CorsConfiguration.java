package com.project.job_Finder.configuration;


import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class CorsConfiguration implements WebMvcConfigurer {
    
    public void addCorsRegistry (CorsConfiguration registry){
        //todo
    }
    
}
