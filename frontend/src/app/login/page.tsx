"use client";
import React, { useState } from "react"
import { Card, CardTitle, CardDescription, CardHeader, CardContent } from "@/components/ui/card";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Mail, LockKeyhole, User, Github, Chrome } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Separator } from "@radix-ui/react-separator";

export default function Login() {
    const [email, setEmail] = useState<string>("");
    const [password, setPassword] = useState("");
    const [fullName, setFullName] = useState<string>("");

    const handleSubmit = (e: React.FormEvent) => {
        console.log("Form submitted");
    }

    const handleSocialLogin = (provider: string) => {
        console.log("Log in with: ", provider);
    }
    return (
        <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
            <Card className="w-full max-w-md">
                <CardHeader className="text-center">
                    <CardTitle className="">JobBot AI</CardTitle>
                    <CardDescription>
                        Your AI-powered job companion
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <Tabs defaultValue="login" className="w-full">
                        <TabsList className="w-full">
                            <TabsTrigger value="login">
                                Login
                            </TabsTrigger>
                            <TabsTrigger value="signup">
                                Sign Up
                            </TabsTrigger>
                        </TabsList>

                        <TabsContent value="login" className="space-y-4">
                            <form onSubmit={handleSubmit} className="space-y-4">
                                <div className="space-y-2">
                                    <Label htmlFor="signin-email">Email</Label>
                                </div>
                                <div className="relative">
                                    <Mail className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                                    <Input
                                        id="signin-email"
                                        type="email"
                                        placeholder="Enter your email"
                                        className="w-full pl-10"
                                        onChange={(e) => setEmail(e.target.value)}
                                        value={email}
                                        required
                                    />
                                </div>
                                <div className="space-y-2">
                                   <Label htmlFor="signin-password">Password</Label>
                                </div>
                                <div className="relative">
                                   <LockKeyhole className="absolute left-3 top-3 h-4 w-4 text-muted-foreground"/>
                                   <Input
                                       id="signin-password"
                                       type="password"
                                       placeholder="Enter your password"
                                       onChange={(e) => setPassword(e.target.value)}
                                       className="w-full pl-10"
                                       value={password}
                                       required
                                   />
                                </div>
                                <Button type="submit" className="w-full">Login</Button>
                            </form>
                        </TabsContent>

                        <TabsContent value="signup" className="space-y-4">
                            <form onSubmit={handleSubmit} className="space-y-4">
                                <div className="space-y-2">
                                    <Label htmlFor="signup-name">Full Name</Label>
                                </div>
                                <div className="relative">
                                  <User className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                                  <Input 
                                    id="signup-name"
                                    type="text"
                                    value={fullName}
                                    onChange={(e) => setFullName(e.target.value)}
                                    placeholder="Enter your full name"
                                    className="w-full pl-10"
                                    required
                                  />  
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="signup-email">Email</Label>
                                </div>
                                <div className="relative">
                                    <Mail className="absolute left-3 top-3 h-4 w-4 text-muted-foreground"/>
                                    <Input
                                        id="signup-email"
                                        className="w-full pl-10"
                                        placeholder="Enter your email"
                                        required
                                    />
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="signup-password">Password</Label>
                                    <div className="relative">
                                        <LockKeyhole className="absolute left-3 top-3 h-4 w-4 text-muted-foreground"/>
                                        <Input
                                            id="signup-password"
                                            type="password"
                                            className="w-full pl-10"
                                            placeholder="Create your password"
                                            required 
                                        />
                                    </div>
                                </div>
                                <Button type="submit" className="w-full">Create Account</Button>
                            </form>
                        </TabsContent>
                    </Tabs>
                    <div className="mt-6">
                        <div className="relative">
                        <div className="absolute inset-0 flex items-center">
                            <Separator className="absolute inset-0 my-auto w-full h-px bg-border" />
                        </div>
                        <div className="relative flex justify-center text-xs uppercase">
                            <span className="bg-background px-2 text-muted-foreground">
                            Or continue with
                            </span>
                        </div>
                        </div>
                        
                        <div className="mt-4 grid grid-cols-2 gap-3">
                        <Button
                            variant="outline"
                            onClick={() => handleSocialLogin('github')}
                            className="w-full"
                        >
                            <Github className="mr-2 h-4 w-4" />
                            GitHub
                        </Button>
                        <Button
                            variant="outline"
                            onClick={() => handleSocialLogin('google')}
                            className="w-full"
                        >
                            <Chrome className="mr-2 h-4 w-4" />
                            Google
                        </Button>
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}