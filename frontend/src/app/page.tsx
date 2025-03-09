'use client';

import { useState } from 'react';
import UploadForm from '@/components/UploadForm';
import SummaryResult from '@/components/SummaryResult';
import { SummarizationResponse, UploadFormData } from '@/types/api';

export default function Home() {
    const [isLoading, setIsLoading] = useState(false);
    const [result, setResult] = useState<SummarizationResponse | null>(null);
    const [error, setError] = useState<string | null>(null);

    const handleSubmit = async (data: UploadFormData) => {
        setIsLoading(true);
        setError(null);

        try {
            const formData = new FormData();
            
            if (data.documentType === 'youtube') {
                formData.append('url', data.youtubeUrl || '');
                const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/summarize/youtube`, {
                    method: 'POST',
                    body: formData,
                });
                
                if (!response.ok) throw new Error('Failed to process YouTube video');
                const result = await response.json();
                setResult(result);
            } else {
                if (data.file) {
                    formData.append('file', data.file);
                    formData.append('document_type', data.documentType);
                    formData.append('max_length', data.maxLength.toString());
                    formData.append('min_length', data.minLength.toString());
                    formData.append('language', data.language);
                    formData.append('export_format', data.exportFormat);

                    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/summarize/file`, {
                        method: 'POST',
                        body: formData,
                    });

                    if (!response.ok) throw new Error('Failed to process file');
                    const result = await response.json();
                    setResult(result);
                }
            }
        } catch (err) {
            setError(err instanceof Error ? err.message : 'An error occurred');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <main className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-4xl mx-auto">
                <div className="text-center mb-12">
                    <h1 className="text-4xl font-bold text-gray-900 mb-4">
                        Text Summarizer AI
                    </h1>
                    <p className="text-lg text-gray-600">
                        Upload a document or provide a YouTube URL to generate an AI-powered summary
                    </p>
                </div>

                <UploadForm onSubmit={handleSubmit} isLoading={isLoading} />

                {error && (
                    <div className="mt-8 p-4 bg-red-50 rounded-lg text-red-700">
                        {error}
                    </div>
                )}

                {result && (
                    <div className="mt-8">
                        <SummaryResult result={result} />
                    </div>
                )}
            </div>
        </main>
    );
}
