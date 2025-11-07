"use client"

import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Building2, MapPin, DollarSign, Briefcase, Search } from "lucide-react";

export default function JobPageComponent() {
    
    const [jobs, setJobs] = useState([]);
    const [selectedIndustries, setSelectedIndustries] = useState([]);

    const mockJobs = [
        { id: 1, title: "Software Engineer", company: "Tech Corp", location: "New York, NY", salary: "80,000 - 120,000", type: "Full-time", link: "##" },
        { id: 2, title: "Data Scientist", company: "Data Inc", location: "San Francisco, CA", salary: "90,000 - 150,000", type: "Full-time", link: "##" },
        { id: 3, title: "Product Manager", company: "Business Solutions", location: "Remote", salary: "70,000 - 100,000", type: "Remote", link: "##" },
        { id: 4, title: "UX Designer", company: "Creative Studio", location: "Manila, PH", salary: "50,000 - 80,000", type: "Full-time", link: "##" },
    ]

    return (
        <div className="min-h-screen bg-background flex flex-col font-sans">
            {/* Header */}
            <header className="border-b border-border bg-card">
                <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                        <Button variant="ghost" className="text-lg sm:text-xl font-semibold">
                            <Search className="h-6 w-6 sm:h-8 sm:w-8 text-primary mr-2" />
                            JobMatchAI
                        </Button>
                    </div>
                </div>
            </header>

            {/* Filter Section */}
            <div className="p-4 sm:p-6 border-b border-border">
                <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="max-w-5xl mx-auto grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
                        <Card className="p-3 sm:p-4 hover:shadow-md transition-shadow">
                            <label className="text-xs font-medium text-muted-foreground mb-2 block flex items-center gap-2">
                                <MapPin className="w-3 h-3" />
                                Location
                            </label>
                            <input
                                type="search"
                                placeholder="Search location..."
                                className="w-full bg-transparent outline-none text-sm"
                            />
                        </Card>

                        <Card className="p-3 sm:p-4 hover:shadow-md transition-shadow">
                            <label className="text-xs font-medium text-muted-foreground mb-2 block flex items-center gap-2">
                                <Briefcase className="w-3 h-3" />
                                Job Type
                            </label>
                            <input
                                type="search"
                                placeholder="Search job type..."
                                className="w-full bg-transparent outline-none text-sm"
                            />
                        </Card>

                        <Card className="p-3 sm:p-4 hover:shadow-md transition-shadow">
                            <label className="text-xs font-medium text-muted-foreground mb-2 block flex items-center gap-2">
                                <span>₱</span>
                                Salary Range
                            </label>
                            <select className="w-full bg-transparent outline-none text-sm">
                                <option>All</option>
                                <option value="0-20000">₱0 - ₱20,000</option>
                                <option value="20000-50000">₱20,000 - ₱50,000</option>
                                <option value="51000-100000">₱51,000 - ₱100,000</option>
                                <option value="100000+">₱100,000+</option>
                            </select>
                        </Card>

                        <Card className="p-3 sm:p-4 hover:shadow-md transition-shadow">
                            <label className="text-xs font-medium text-muted-foreground mb-2 block flex items-center gap-2">
                                <Building2 className="w-3 h-3" />
                                Industry
                            </label>
                            <select className="w-full bg-transparent outline-none text-sm">
                                <option>All industries</option>
                                <option value="it">IT / Software</option>
                                <option value="finance">Finance</option>
                                <option value="health">Healthcare</option>
                                <option value="education">Education</option>
                                <option value="manufacturing">Manufacturing</option>
                            </select>
                        </Card>
                    </div>
                </div>
            </div>

            {/* Main Content */}
            <main className="flex-1 px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
                <div className="max-w-5xl mx-auto">
                    <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6 gap-4">
                        <div>
                            <h2 className="text-2xl sm:text-3xl font-bold">Job Listings</h2>
                            <p className="text-sm text-muted-foreground mt-1">{mockJobs.length} jobs found</p>
                        </div>
                        <select className="px-4 py-2 border rounded-lg text-sm bg-card w-full sm:w-auto">
                            <option>Most Relevant</option>
                            <option>Newest First</option>
                            <option>Highest Salary</option>
                        </select>
                    </div>

                    <div className="space-y-4 sm:space-y-6">
                        {mockJobs.map((job) => (
                            <Card key={job.id} className="hover:shadow-lg transition-shadow">
                                <CardContent className="p-4 sm:p-6">
                                    <div className="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-4">
                                        {/* Job Info */}
                                        <div className="flex-1 space-y-4">
                                            <div>
                                                <CardTitle className="text-xl sm:text-2xl mb-3 leading-relaxed">{job.title}</CardTitle>
                                                <div className="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4 text-sm text-muted-foreground mb-3">
                                                    <span className="flex items-center gap-1.5">
                                                        <Building2 className="w-4 h-4" />
                                                        {job.company}
                                                    </span>
                                                    <span className="flex items-center gap-1.5">
                                                        <MapPin className="w-4 h-4" />
                                                        {job.location}
                                                    </span>
                                                </div>
                                            </div>

                                            <CardDescription className="text-sm leading-relaxed">
                                                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.
                                            </CardDescription>

                                            <div className="flex flex-wrap gap-2 pt-2">
                                                <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-primary/10 text-primary">
                                                    <Briefcase className="w-3 h-3 mr-1" />
                                                    {job.type}
                                                </span>
                                                <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-primary/10 text-primary">
                                                    ₱ {job.salary}
                                                </span>
                                            </div>
                                        </div>

                                        {/* Apply Button */}
                                        <div className="flex items-start">
                                            <Button 
                                                className="w-full sm:w-auto lg:min-w-[120px]"
                                                onClick={() => window.open(job.link, '_blank', 'noopener,noreferrer')}
                                            >
                                                Apply Now
                                            </Button>
                                        </div>
                                    </div>
                                </CardContent>
                            </Card>
                        ))}
                    </div>

                    {/* Load More */}
                    <div className="mt-8 text-center">
                        <Button variant="outline" size="lg" className="w-full sm:w-auto">
                            Load More Jobs
                        </Button>
                    </div>
                </div>
            </main>
        </div>
    );
}