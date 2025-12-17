"use client"
import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { User, Briefcase, GraduationCap, MapPin, DollarSign, Home, LogOut, Plus, X, Search, Upload, FileText, ChevronRight } from 'lucide-react';
import { LoadingOverlay } from '@/components/ui/loadingoverlay';


export default function ProfilePage() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [showMethodChoice, setShowMethodChoice] = useState(true);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [isProcessingCV, setIsProcessingCV] = useState(false);
  const [isProfileUploaded, setIsProfileUploaded] = useState<boolean>(false);
  const [matchJobs, setMatchJobs] = useState<Array<any>>([]);

  // Load existing profile on component mount

  const handleMethodChoice = (method: 'manual' | 'upload') => {
    setShowMethodChoice(true);
    if (method === 'upload') {
      // Trigger file input
      document.getElementById('cv-upload')?.click();
    }
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    // Validate file type
    const validTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    if (!validTypes.includes(file.type)) {
      alert('Please upload a PDF or Word document');
      return;
    }

    // Validate file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      alert('File size must be less than 5MB');
      return;
    }

    setUploadedFile(file);
    console.log('Uploaded file:', file);
    setIsProfileUploaded(true);
    setIsProcessingCV(true);

    try {
      // setFormData(extractedData);
    } catch (error) {
      console.error('Error processing CV:', error);
      alert('Error processing CV. Please try again later.');
    } finally {
      setIsProcessingCV(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
  
    try {
      const formData = new FormData();
  
      if (uploadedFile) {
        formData.append("resume_pdf", uploadedFile);
      } else {
        alert("Please upload your resume first.");
        return;
      }
      
      //add auth soon
      const response = await fetch("https://job-matcher-api-1019829241078.asia-southeast1.run.app/match_with_gcs", {
        method: "POST",
        body: formData,
      });
      
      if (!response.ok) throw new Error(`Server error: ${response.status}`);
      
      const results = await response.json();
      console.log("API Response:", results);
      
      // Save the sorted job array (not the wrapper object)
      sessionStorage.setItem("jobResults", JSON.stringify(results.all_matches));
      
      // Redirect to results page
      router.push("/results");
      
    } catch (error) {
      console.error("Error uploading files:", error);
    } finally {
      setIsLoading(false);
    }
  };

  // Method choice screen
    return (
      <div className="min-h-screen bg-background">
        {isLoading && <LoadingOverlay/>}
        <header className="border-b border-border bg-card">
          <div className="container mx-auto px-4 py-4 flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Button onClick={() => router.push('/')} variant="ghost" className="text-xl font-semibold">
                <Search className="h-8 w-8 text-primary" />
                JobMatchAI
              </Button>
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

        <main className="container mx-auto px-4 py-16 max-w-4xl">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold">Upload Your Resume or CV</h2>
        </div>

        <div className="grid md:grid-cols-2 gap-10 max-w-3xl mx-auto">
          {/* Upload CV Option */}
          <Card
            className="cursor-pointer hover:border-primary transition-colors flex flex-col justify-center"
            onClick={() => handleMethodChoice('upload')}
          >
            <CardContent className="p-8 text-center flex flex-col items-center">
              <div className="mb-6 flex justify-center">
                <div className="p-5 bg-primary/10 rounded-full">
                  <Upload className="h-10 w-10 text-primary" />
                </div>
              </div>
              <h3 className="text-xl font-semibold mb-3">Upload Your CV</h3>
              <p className="text-muted-foreground mb-6 max-w-xs">
                {isProcessingCV
                  ? 'Our AI is extracting information from your resume'
                  : 'Let our AI extract information from your resume automatically'}
              </p>
              <div className="flex items-center justify-center space-x-2 text-sm text-muted-foreground mb-8">
                <FileText className="h-5 w-5" />
                <span className="text-green-600">PDF, DOC, DOCX (Max 5MB)</span>
              </div>
              <Button className="w-full max-w-xs" size="lg">
                Upload CV/Resume
                <ChevronRight className="ml-2 h-5 w-5" />
              </Button>
            </CardContent>
          </Card>

          {/* Single card for status and buttons */}
          <Card className="flex flex-col justify-center p-8 max-w-md mx-auto hover:border-primary transition-colors">
            <p className="mb-6 text-center text-lg font-medium">
              {isProfileUploaded ? 'Profile Uploaded' : 'Please upload profile'}
            </p>
            <p className="mb-8 text-center text-muted-foreground truncate">
              File name: {uploadedFile?.name || 'None'}
            </p>
            <div className="flex justify-center space-x-6">
              <Button className="w-28 cursor-pointer" size="lg" onClick={handleSubmit} disabled={!isProfileUploaded || isProcessingCV}>
                Submit
              </Button>
            </div>
          </Card>
        </div>

        {/* Hidden file input */}
        <input
          id="cv-upload"
          type="file"
          accept=".pdf,.doc,.docx"
          onChange={handleFileUpload}
          className="hidden"
        />
      </main>

      </div>
    );
  }
