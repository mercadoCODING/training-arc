"use client"
import React, { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardDescription, CardTitle } from "@/components/ui/card"
import { Briefcase, TrendingUp } from "lucide-react"
import { Search, User } from "lucide-react"
import { useRouter } from "next/navigation"

export default function Dashboard() {
    const router = useRouter();
    const [hasProfile, setHasProfile] = useState(false);

    const jobstats = [
        { label: "New Jobs Today" , value: 2345, icon: TrendingUp },
    ]

    return (
        <div className="min-h-screen bg-background">
            {/* Header */}
            <header className="border-b border-border bg-card">
                <div className="container mx-auto px-4 py-4 flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                        <Button onClick={() => router.push('/')} variant="ghost" className="text-lg sm:text-xl font-semibold p-2">
                            <Search className="h-6 w-6 sm:h-8 sm:w-8 text-primary" />
                            <span className="hidden sm:inline ml-2">JobMatchAI</span>
                            <span className="sm:hidden ml-2">JobMatch</span>
                        </Button>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="px-4 sm:px-6 md:px-16 lg:px-32 xl:px-60 pt-5 pb-8">
                <div className="mb-6 sm:mb-8">
                    <h2 className="text-2xl sm:text-3xl mb-2">Welcome to JobMatch AI!</h2>
                    <p className="text-sm sm:text-base text-muted-foreground">AI-powered job matching based on your experience and skills.</p>
                </div>

                {/* Profile and Status Alert */}
                {!hasProfile && (
                    <Card className="mb-6 sm:mb-5 border-orange-200 bg-orange-50 dark:border-orange-800 dark:bg-orange-950">
                        <CardHeader>
                            <CardTitle className="flex items-center space-x-2 text-orange-800 dark:text-orange-200 text-base sm:text-lg">
                                <User className="h-5 w-5" />
                                <span>Complete Your Profile</span>
                            </CardTitle>
                            <CardDescription className="text-orange-700 dark:text-orange-300 text-sm">
                                Upload your profile to get personalized job recommendations.
                            </CardDescription>
                        </CardHeader>
                        <CardContent>
                            <Button onClick={() => router.push('profile')} className="bg-orange-600 hover:bg-orange-700 w-full sm:w-auto">
                                <User className="mr-2 h-4 w-4" />
                                Upload CV/Resume
                            </Button>
                        </CardContent>
                    </Card>
                )}

                {/* Status Cards */}
                <div className="mb-6 sm:mb-6 grid grid-cols-1 sm:grid-cols-1 gap-4">
                    {jobstats.map((stat, index) => (
                        <Card className="w-full" key={index}>
                            <CardContent className="p-4 sm:p-6">
                                <div className="flex items-center space-x-2">
                                    <stat.icon className="h-5 w-5 text-muted-foreground" />
                                    <div className="flex-1">
                                        <p className="text-sm text-muted-foreground">{stat.label}</p>
                                        <p className="text-xl sm:text-2xl">{stat.value}</p>
                                    </div>
                                </div>
                            </CardContent>
                        </Card>
                    ))}

                    {/* Browse Jobs */}
                    <Card>
                        <CardHeader className="pb-3">
                            <CardTitle className="flex items-center space-x-2 text-base sm:text-lg">
                                <Briefcase className="h-5 w-5" />
                                <span>Browse Jobs</span>
                            </CardTitle>
                            <CardDescription className="text-sm">
                                {hasProfile ? 
                                    "Find jobs matched to your experience and preference" 
                                    : "Browse Available Job opportunities"
                                }
                            </CardDescription>
                        </CardHeader>
                        <CardContent>
                            <Button onClick={() => router.push('/jobs')} className="w-full sm:w-auto">
                                <Search className="mr-2 h-4 w-4" />
                                Browse Jobs
                            </Button>
                        </CardContent>
                    </Card>
                </div>

            </main>
        </div>
    )
}