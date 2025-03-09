import { SummarizationResponse } from '@/types/api';
import Button from './Button';

interface SummaryResultProps {
    result: SummarizationResponse;
}

export default function SummaryResult({ result }: SummaryResultProps) {
    const handleDownload = () => {
        if (result.export_url) {
            window.open(`${process.env.NEXT_PUBLIC_API_URL}${result.export_url}`, '_blank');
        }
    };

    return (
        <div className="bg-white shadow rounded-lg p-6 space-y-4">
            <div>
                <h3 className="text-lg font-medium text-gray-900">Summary</h3>
                <p className="mt-2 text-gray-600 whitespace-pre-wrap">{result.summary}</p>
            </div>

            <div className="grid grid-cols-2 gap-4 text-sm text-gray-500">
                <div>
                    <span className="font-medium">Original Length:</span>{' '}
                    {result.original_length} characters
                </div>
                <div>
                    <span className="font-medium">Summary Length:</span>{' '}
                    {result.summary_length} characters
                </div>
                <div>
                    <span className="font-medium">Processing Time:</span>{' '}
                    {result.processing_time.toFixed(2)} seconds
                </div>
                <div>
                    <span className="font-medium">Document Type:</span>{' '}
                    {result.document_type.toUpperCase()}
                </div>
            </div>

            {result.export_url && (
                <Button onClick={handleDownload} variant="outline" className="w-full">
                    Download Summary
                </Button>
            )}
        </div>
    );
} 