"use client";

import React from "react";

interface Job {
  title: string;
  company?: string;
  location?: string;
  salary?: string | null;
  link?: string;
  cosine_score: number;
  description?: string;
}

interface TopJobsProps {
  jobs: Job[];
}

export default function TopJobs({ jobs }: TopJobsProps) {
  if (!jobs || jobs.length === 0) {
    return <p className="text-gray-500">No job matches found.</p>;
  }

  // Only take the top 5 jobs
  const topJobs = jobs.slice(0, 20);

  return (
    <div className="mt-10">
      <h2 className="text-2xl font-bold mb-6">Top Job Matches</h2>
      <ul className="space-y-6">
        {topJobs.map((job, index) => (
          <li
            key={index}
            className="p-5 border border-gray-200 rounded-xl shadow-sm bg-white hover:shadow-md transition-shadow duration-200"
          >
            <div className="flex justify-between items-start">
              <div>
                <h3 className="text-xl font-semibold">{job.title}</h3>
                {job.company && (
                  <p className="text-sm text-gray-700">{job.company}</p>
                )}
                {job.location && (
                  <p className="text-sm text-gray-500">{job.location}</p>
                )}
              </div>
              <span className="text-sm text-blue-600 font-medium">
                {(job.cosine_score * 100).toFixed(1)}%
              </span>
            </div>

            {job.salary && (
              <p className="mt-2 text-sm text-green-700 font-medium">
                💰 {job.salary}
              </p>
            )}

            <p className="mt-3 text-gray-600 text-sm line-clamp-3">
              {job.description?.slice(0, 250)}...
            </p>

            {job.link && (
              <a
                href={job.link}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-block mt-4 text-sm text-white bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg"
              >
                View Job →
              </a>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
