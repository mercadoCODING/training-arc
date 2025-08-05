"use client"
import React, { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardAction, CardContent, CardHeader, CardDescription, CardTitle } from "@/components/ui/card"
import { Badge } from "lucide-react"
import { Settings, LogOut, Search, User } from "lucide-react"
import { useRouter } from "next/navigation"

export default function Dashboard() {
    const router = useRouter();
    const [hasProfile, setHasProfile] = useState(false);

    const onLogout = () => {
        console.log("Logout logic");
    }

    const handleProfile = () => {
        console.log("Navigate to profile function");
    }

    return (
        <div className="min-h-screen bg-background">
            {/* Header */}
            <header className="border-b border-border bg-card">
                <div className="container mx-auto px-4 py-4 flex items-center justify-between">
                <div className="flex items-center space-x-2">
                    <Search className="h-8 w-8 text-primary" />
                    <h1 className="text-xl">JobMatch AI</h1>
                </div>
                <div className="flex items-center space-x-2">
                    <Button variant="ghost" onClick={handleProfile}>
                    <User className="mr-2 h-4 w-4" />
                    </Button>
                    Profile
                    <Button variant="ghost" onClick={onLogout}>
                    <LogOut className="mr-2 h-4 w-4" />
                    Logout
                    </Button>
                </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="pt-5 pr-60 pl-60">
                <div mb-8>
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
                        Set up your experience and preferences to get personalized job recommendations.
                    </CardDescription>
                    </CardHeader>
                    <CardContent>
                    <Button onClick={() => router.push('profile')} className="bg-orange-600 hover:bg-orange-700">
                        <User className="mr-2 h-4 w-4" />
                        Setup Profile
                    </Button>
                    </CardContent>
                </Card>
                )}
            </main>
        </div >
    )
}