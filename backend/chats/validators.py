from django.core.exceptions import ValidationError

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

ALLOWED_FILE_TYPES = {
    'pdf': 'application/pdf',
    'doc': 'application/msword',
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'txt': 'text/plain',
    'zip': 'application/zip',
    'rar': 'application/x-rar-compressed',
    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'csv': 'text/csv',
}

def validate_file_upload(file):
    """Validate file size and type"""
    if file.size > MAX_FILE_SIZE:
        raise ValidationError(f'File size cannot exceed {MAX_FILE_SIZE / (1024*1024)}MB')
    
    file_ext = file.name.split('.')[-1].lower()
    if file_ext not in ALLOWED_FILE_TYPES:
        raise ValidationError(f'File type .{file_ext} is not allowed')
    
    return True
