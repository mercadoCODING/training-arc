"use client";

import Image from "next/image";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Search, Brain, Target, Zap } from "lucide-react";
import Link from "next/link";

export default function Home() {


  return (
    <div className="min-h-screen bg-background flex flex-col font-sans">
      {/* Header */}
      <header className="border-b border-border bg-card">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Search className="h-6 w-6 text-primary" />
            <span className="text-lg font-semibold">JobMatch.AI</span>
          </div>
          {/* <Button variant="ghost">Sign In</Button> */}
        </div>
      </header>

      {/* Main */}
      <main className="flex-1 flex items-center justify-center p-8">
        <div className="max-w-3xl mx-auto text-center space-y-12">
          {/* Hero Title */}
          <div className="space-y-4">
            <h1 className="text-6xl md:text-7xl font-bold tracking-tight">
              JobMatch<span className="text-primary">.AI</span>
            </h1>
            <p className="text-muted-foreground text-lg">
              Revolutionizing job search with artificial intelligence.
            </p>
          </div>

          {/* Feature Steps */}
          <ol className="space-y-3 text-left max-w-lg mx-auto">
            {[
              "Get matched with jobs by sharing your experience and skills.",
              "AI analyzes your profile and finds perfect job matches.",
              "Apply to jobs with higher success rates and better fit.",
            ].map((step, idx) => (
              <li key={idx} className="flex items-start space-x-3">
                <span className="flex-shrink-0 w-6 h-6 bg-primary text-primary-foreground rounded-full flex items-center justify-center text-sm">
                  {idx + 1}
                </span>
                <span className="text-sm text-muted-foreground">{step}</span>
              </li>
            ))}
          </ol>

          {/* CTA Buttons */}
          <Link href={"/profile"}>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" className="px-8 py-3 rounded-full">
                <Zap className="mr-2 h-4 w-4" />
                Get Started
              </Button>
              {/* <Button variant="ghost" size="lg" className="px-8 py-3">
                What's Unique About Us
              </Button> */}
            </div>
          </Link>

          {/* Feature Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-16">
            <FeatureCard
              icon={<Brain className="h-8 w-8 text-primary mx-auto mb-3" />}
              title="AI-Powered Matching"
              description="Smart algorithms analyze your experience to find the best job matches."
            />
            <FeatureCard
              icon={<Target className="h-8 w-8 text-primary mx-auto mb-3" />}
              title="Experience-Based Filtering"
              description="Jobs filtered based on your actual skills and career background."
            />
            <FeatureCard
              icon={<Search className="h-8 w-8 text-primary mx-auto mb-3" />}
              title="Real-Time Job Scraping"
              description="Fresh job listings from multiple sources, updated continuously."
            />
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-border bg-card text-center py-4 text-sm text-muted-foreground">
        © 2025 JobMatch AI. All rights reserved.
      </footer>
    </div>
  );
}

function FeatureCard({
  icon,
  title,
  description,
}: {
  icon: React.ReactNode;
  title: string;
  description: string;
}) {
  return (
    <Card className="border-border/50">
      <CardHeader className="text-center">
        {icon}
        <CardTitle className="text-sm">{title}</CardTitle>
        <CardDescription>{description}</CardDescription>
      </CardHeader>
    </Card>
  );
}
