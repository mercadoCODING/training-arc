"use client";

import { useEffect, useState } from "react";
import TopJobs from "../../components/ui/topjobs";
import { Home, Search } from "lucide-react";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import router from "next/router";

export default function ResultsPage() {
  const [jobs, setJobs] = useState([]);

  useEffect(() => {
    const data = sessionStorage.getItem("jobResults");
    if (data) setJobs(JSON.parse(data));
  }, []);

  return (
    <div className="min-h-screen bg-background">
    <header className="border-b border-border bg-card">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <div className="flex items-center space-x-2">
        <Link href = "/">
          <Button variant="ghost" className="text-xl font-semibold">
            <Search className="h-8 w-8 text-primary" />
            JobMatchAI
          </Button>
          </Link>
        </div>
        <div className="flex items-center space-x-2">
          <Button variant="ghost" size="sm" asChild>
            <Link href="/dashboard">
              <Home className="mr-2 h-4 w-4" />
              Dashboard
            </Link>
          </Button>
        </div>
      </div>
    </header>

      {/* Main */}
      <main className="flex-1 p-10">
        <div className="max-w-5xl mx-auto space-y-8">
          <h1 className="text-3xl font-bold mb-4">Your AI Job Matches</h1>
          {jobs.length > 0 ? (
            <TopJobs jobs={jobs} />
          ) : (
            <p className="text-muted-foreground text-center">
              No job results found. Try running a new search.
            </p>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-border bg-card text-center py-4 text-sm text-muted-foreground">
        © 2025 JobMatch AI. All rights reserved.
      </footer>
    </div>
  );
}
