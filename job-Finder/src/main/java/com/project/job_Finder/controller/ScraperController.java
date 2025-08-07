package com.project.job_Finder.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ScraperController {
    
    //TODO 
    @GetMapping("/scrape-site")
    public String fetchWebsiteFromPython(){
        //sasalohin ko nalang ung transfer
        return "scape-site";
    }
}
