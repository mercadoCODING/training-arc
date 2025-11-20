'use client';
import React from 'react';

export const LoadingOverlay = () => (
  <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50">
    <h2 className="text-white text-xl font-bold animate-pulse text-center max-w-xs">
      Job-Finder AI is now computing your best jobs.<br />Please wait...
    </h2>
  </div>
);