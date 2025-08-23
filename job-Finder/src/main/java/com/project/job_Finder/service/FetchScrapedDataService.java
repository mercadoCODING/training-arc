package com.project.job_Finder.service;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import com.project.job_Finder.model.ScrapedData;


@Service
public class FetchScrapedDataService {

    private final RestTemplate restTemplate = new RestTemplate();
    private final String pythonEndpoint = "";


    public ScrapedData fetchData(){
        return restTemplate.getForObject(pythonEndpoint, ScrapedData.class);
    }

}
