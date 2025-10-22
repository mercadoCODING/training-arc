"use client"
import React, { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardAction, CardContent, CardHeader, CardDescription, CardTitle } from "@/components/ui/card"
import { Badge, Briefcase, TrendingUp } from "lucide-react"
import { Settings, LogOut, Search, User } from "lucide-react"
import { useRouter } from "next/navigation"

export default function Dashboard() {
    const router = useRouter();
    const [hasProfile, setHasProfile] = useState(false);

    // const onLogout = () => {
    //     console.log("Logout logic");
    // }

    // const handleProfile = () => {
    //     console.log("Navigate to profile function");
    // }

    const jobstats = [
        { label: "New Jobs Today" , value: 2345, icon: TrendingUp },
    ]

    return (
        <div className="min-h-screen bg-background">
            {/* Header */}
            <header className="border-b border-border bg-card">
                <div className="container mx-auto px-4 py-4 flex items-center justify-between">
                <div className="flex items-center space-x-2">
                    <Button onClick={() => router.push('/')} variant="ghost" className="text-xl font-semibold">
                        <Search className="h-8 w-8 text-primary" />
                        JobMatchAI
                    </Button>
                </div>
                <div className="flex items-center space-x-2">
                    {/* <Button variant="ghost" onClick={handleProfile}>
                    <User className="mr-2 h-4 w-4" />
                    </Button>
                    Profile
                    <Button variant="ghost" onClick={onLogout}>
                    <LogOut className="mr-2 h-4 w-4" />
                    Logout
                    </Button> */}
                </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="pt-5 pr-60 pl-60">
                <div className="mb-8">
                    <h2 className="text-3xl mb-2">Welcome to JobMatch AI!</h2>
                    <p className="text-muted-foreground">AI-powered job matching based on your experience and skills.</p>
                </div>

                {/* Profile and Status Alert */}
                {!hasProfile && (
                <Card className="mb-8 mt-8 border-orange-200 bg-orange-50 dark:border-orange-800 dark:bg-orange-950">
                    <CardHeader>
                    <CardTitle className="flex items-center space-x-2 text-orange-800 dark:text-orange-200">
                        <User className="h-5 w-5" />
                        <span>Complete Your Profile</span>
                    </CardTitle>
                    <CardDescription className="text-orange-700 dark:text-orange-300">
                       Upload your profile to get personalized job recommendations.
                    </CardDescription>
                    </CardHeader>
                    <CardContent>
                    <Button onClick={() => router.push('profile')} className="bg-orange-600 hover:bg-orange-700">
                        <User className="mr-2 h-4 w-4" />
                        Upload CV/Resume
                    </Button>
                    </CardContent>
                </Card>
                )}

                {/* Status Cards */}
                <div className="mb-8">
                    {jobstats.map((stat, index) => (
                        <Card className="w-full" key={index}>
                            <CardContent className="p-6">
                                <div className="flex items-center space-x-2">
                                    <stat.icon className="h-5 w-5 text-muted-foreground" />
                                    <div className="flex-1">
                                        <p className="text-sm text-muted-foreground">{stat.label}</p>
                                        <p className="text-2xl">{stat.value}</p>
                                    </div>
                                </div>
                            </CardContent>
                        </Card>
                    ))}
                </div>

                {/* Browse Jobs */}
                    <Card>
                        <CardHeader>
                            <CardTitle className="flex items-center space-x-2">
                                <Briefcase className="h-5 w-5" />
                                <span>Browse Jobs</span>
                            </CardTitle>
                            <CardDescription>
                                {hasProfile ? 
                                    "Find jobs matched to your experience and preference" 
                                    : "Browse Available Job opportunities"
                                }
                            </CardDescription>
                        </CardHeader>
                        <CardContent>
                            <Button>
                                <Search />
                                Browse Jobs
                            </Button>
                        </CardContent>
                    </Card>

            </main>
        </div >
    )
}