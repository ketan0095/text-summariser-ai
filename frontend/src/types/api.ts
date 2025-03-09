export enum DocumentType {
    PDF = "pdf",
    DOCX = "docx",
    AUDIO = "audio",
    YOUTUBE = "youtube",
    TEXT = "text",
}

export enum ExportFormat {
    PDF = "pdf",
    TEXT = "text",
}

export interface SummarizationResponse {
    summary: string;
    original_length: number;
    summary_length: number;
    processing_time: number;
    document_type: DocumentType;
    export_url?: string;
    timestamp: string;
}

export interface UploadFormData {
    file?: File;
    youtubeUrl?: string;
    documentType: DocumentType;
    maxLength: number;
    minLength: number;
    language: string;
    exportFormat: ExportFormat;
} 