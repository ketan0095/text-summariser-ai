import { useState, FormEvent } from 'react';
import { DocumentType, ExportFormat, UploadFormData } from '@/types/api';
import Button from './Button';

interface UploadFormProps {
    onSubmit: (data: UploadFormData) => Promise<void>;
    isLoading: boolean;
}

export default function UploadForm({ onSubmit, isLoading }: UploadFormProps) {
    const [documentType, setDocumentType] = useState<DocumentType>(DocumentType.PDF);
    const [file, setFile] = useState<File | null>(null);
    const [youtubeUrl, setYoutubeUrl] = useState('');
    const [maxLength, setMaxLength] = useState(500);
    const [minLength, setMinLength] = useState(100);
    const [language, setLanguage] = useState('en');
    const [exportFormat, setExportFormat] = useState<ExportFormat>(ExportFormat.PDF);

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();
        if (documentType === DocumentType.YOUTUBE && !youtubeUrl) {
            alert('Please enter a YouTube URL');
            return;
        }
        if (documentType !== DocumentType.YOUTUBE && !file) {
            alert('Please select a file');
            return;
        }

        await onSubmit({
            file: file || undefined,
            youtubeUrl: youtubeUrl || undefined,
            documentType,
            maxLength,
            minLength,
            language,
            exportFormat,
        });
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-6 max-w-2xl mx-auto">
            <div className="space-y-4">
                <div>
                    <label className="block text-sm font-medium text-gray-700">Document Type</label>
                    <select
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                        value={documentType}
                        onChange={(e) => setDocumentType(e.target.value as DocumentType)}
                    >
                        {Object.values(DocumentType).map((type) => (
                            <option key={type} value={type}>
                                {type.toUpperCase()}
                            </option>
                        ))}
                    </select>
                </div>

                {documentType === DocumentType.YOUTUBE ? (
                    <div>
                        <label className="block text-sm font-medium text-gray-700">YouTube URL</label>
                        <input
                            type="url"
                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                            value={youtubeUrl}
                            onChange={(e) => setYoutubeUrl(e.target.value)}
                            placeholder="https://www.youtube.com/watch?v=..."
                        />
                    </div>
                ) : (
                    <div>
                        <label className="block text-sm font-medium text-gray-700">File</label>
                        <input
                            type="file"
                            className="mt-1 block w-full"
                            onChange={(e) => setFile(e.target.files?.[0] || null)}
                            accept={`.${documentType}`}
                        />
                    </div>
                )}

                <div className="grid grid-cols-2 gap-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700">Min Length</label>
                        <input
                            type="number"
                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                            value={minLength}
                            onChange={(e) => setMinLength(Number(e.target.value))}
                            min="50"
                            max="1000"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700">Max Length</label>
                        <input
                            type="number"
                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                            value={maxLength}
                            onChange={(e) => setMaxLength(Number(e.target.value))}
                            min="100"
                            max="2000"
                        />
                    </div>
                </div>

                <div>
                    <label className="block text-sm font-medium text-gray-700">Language</label>
                    <input
                        type="text"
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                        value={language}
                        onChange={(e) => setLanguage(e.target.value)}
                        placeholder="en"
                    />
                </div>

                <div>
                    <label className="block text-sm font-medium text-gray-700">Export Format</label>
                    <select
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                        value={exportFormat}
                        onChange={(e) => setExportFormat(e.target.value as ExportFormat)}
                    >
                        {Object.values(ExportFormat).map((format) => (
                            <option key={format} value={format}>
                                {format.toUpperCase()}
                            </option>
                        ))}
                    </select>
                </div>
            </div>

            <Button type="submit" isLoading={isLoading} className="w-full">
                Generate Summary
            </Button>
        </form>
    );
} 