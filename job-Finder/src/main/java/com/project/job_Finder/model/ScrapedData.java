package com.project.job_Finder.model;

//model
public class ScrapedData {
    private final String link;
    private final String jobName;
    private final String salary;

    //default constructor

    public ScrapedData() {
        this.link = "";
        this.jobName = "";
        this.salary = "";
    }
    
    //Constructor
    public ScrapedData(String link, String jobName, String salary){
        this.link = link;
        this.jobName = jobName;
        this.salary = salary;
    }

  
    public String getLink() {
        return link;
    }

    public String getJobName() {
        return jobName;
    }

    public String getSalary() {
        return salary;
    }


}
