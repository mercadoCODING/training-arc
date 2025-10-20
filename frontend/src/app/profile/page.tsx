"use client"
import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Checkbox } from '@/components/ui/checkbox';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { User, Briefcase, GraduationCap, MapPin, DollarSign, Home, LogOut, Plus, X, Search, Upload, FileText, ChevronRight } from 'lucide-react';

interface ProfileData {
  personalInfo: {
    fullName: string;
    email: string;
    phone: string;
    location: string;
  };
  experience: {
    yearsOfExperience: string;
    currentPosition: string;
    industry: string;
    experienceLevel: string;
  };
  education: {
    degree: string;
    field: string;
    university: string;
    graduationYear: string;
  };
  skills: string[];
  preferences: {
    desiredPosition: string;
    preferredLocation: string;
    salaryRange: string;
    jobType: string;
    workArrangement: string;
  };
}

export default function ProfilePage() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [showMethodChoice, setShowMethodChoice] = useState(true);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [isProcessingCV, setIsProcessingCV] = useState(false);
  const [isProfileUploaded, setIsProfileUploaded] = useState<boolean>(false);

  const [formData, setFormData] = useState<ProfileData>({
    personalInfo: {
      fullName: '',
      email: '',
      phone: '',
      location: ''
    },
    experience: {
      yearsOfExperience: '',
      currentPosition: '',
      industry: '',
      experienceLevel: ''
    },
    education: {
      degree: '',
      field: '',
      university: '',
      graduationYear: ''
    },
    skills: [],
    preferences: {
      desiredPosition: '',
      preferredLocation: '',
      salaryRange: '',
      jobType: '',
      workArrangement: ''
    }
  });

  const [newSkill, setNewSkill] = useState('');

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
      // Simulate AI processing of CV
      // In a real app, this would call an API to extract data from the CV
      await new Promise(resolve => setTimeout(resolve, 2000));

      // // Mock extracted data
      // const extractedData: ProfileData = {
      //   personalInfo: {
      //     fullName: 'John Doe',
      //     email: 'john.doe@example.com',
      //     phone: '+63 912 345 6789',
      //     location: 'Manila, Philippines'
      //   },
      //   experience: {
      //     yearsOfExperience: '3-5',
      //     currentPosition: 'Senior Software Developer',
      //     industry: 'Technology',
      //     experienceLevel: 'senior'
      //   },
      //   education: {
      //     degree: "Bachelor's in Computer Science",
      //     field: 'Computer Science',
      //     university: 'University of the Philippines',
      //     graduationYear: '2018'
      //   },
      //   skills: ['React', 'TypeScript', 'Node.js', 'Python', 'AWS', 'Docker'],
      //   preferences: {
      //     desiredPosition: 'Senior Software Engineer',
      //     preferredLocation: 'Manila or Remote',
      //     salaryRange: '80k-100k',
      //     jobType: 'full-time',
      //     workArrangement: 'hybrid'
      //   }
      // };

      // setFormData(extractedData);
    } catch (error) {
      console.error('Error processing CV:', error);
      alert('Error processing CV. Please try manual entry.');
    } finally {
      setIsProcessingCV(false);
    }
  };

  const handleInputChange = (section: keyof ProfileData, field: string, value: string) => {
    setFormData(prev => ({
      ...prev,
      [section]: {
        ...(prev[section] as any),
        [field]: value
      }
    }));
  };

  // const addSkill = () => {
  //   if (newSkill.trim() && !formData.skills.includes(newSkill.trim())) {
  //     setFormData(prev => ({
  //       ...prev,
  //       skills: [...prev.skills, newSkill.trim()]
  //     }));
  //     setNewSkill('');
  //   }
  // };

  // const removeSkill = (skillToRemove: string) => {
  //   setFormData(prev => ({
  //     ...prev,
  //     skills: prev.skills.filter(skill => skill !== skillToRemove)
  //   }));
  // };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      localStorage.setItem('userProfile', JSON.stringify(formData));
      await new Promise(resolve => setTimeout(resolve, 1000));
      router.push('/dashboard');
    } catch (error) {
      console.error('Error saving profile:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('userProfile');
    router.push('/login');
  };

  // Method choice screen
    return (
      <div className="min-h-screen bg-background">
        <header className="border-b border-border bg-card">
          <div className="container mx-auto px-4 py-4 flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Search className="h-8 w-8 text-primary" />
              <h1 className="text-xl font-semibold">JobMatch AI</h1>
            </div>
            <div className="flex items-center space-x-2">
              <Button variant="ghost" size="sm" asChild>
                <Link href="/dashboard">
                  <Home className="mr-2 h-4 w-4" />
                  Dashboard
                </Link>
              </Button>
              <Button variant="ghost" size="sm" onClick={handleLogout}>
                <LogOut className="mr-2 h-4 w-4" />
                Logout
              </Button>
            </div>
          </div>
        </header>

        <main className="container mx-auto px-4 py-16 max-w-4xl">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold">Build Your Professional Profile</h2>
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
          <Card className="flex flex-col justify-center p-8 max-w-xs mx-auto cursor-pointer hover:border-primary transition-colors">
            <p className="mb-6 text-center text-lg font-medium">
              {isProfileUploaded ? 'Profile Uploaded' : 'Please upload profile'}
            </p>
            <p className="mb-8 text-center text-muted-foreground truncate">
              File name: {uploadedFile?.name || 'None'}
            </p>
            <div className="flex justify-center space-x-6">
              <Button variant="secondary" className="w-28 hover:bg-orange-600" size="lg">
                Cancel
              </Button>
              <Button className="w-28" size="lg">
                Confirm
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
