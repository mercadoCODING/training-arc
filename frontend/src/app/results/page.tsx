"use client";
import { useEffect, useState } from "react";
import TopJobs from "../../components/ui/TopJobs";

export default function ResultsPage() {
  const [jobs, setJobs] = useState([]);

  useEffect(() => {
    const data = sessionStorage.getItem("jobResults");
    if (data) setJobs(JSON.parse(data));
  }, []);

  return (
    <div className="min-h-screen p-10 bg-background">
      <h1 className="text-3xl font-bold mb-8">Your AI Job Matches</h1>
      <TopJobs jobs={jobs} />
    </div>
  );
}
