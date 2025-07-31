import os

CLEANUP_TIME = 24

MEMORY_LIMIT = 512

DOWNLOADS_FOLDER = os.path.expanduser("~/Downloads")

CATEGORIZED_FOLDERS = {
    'images': ['.jpg', '.jpeg', '.png', '.gif'],
    'documents': ['.pdf', '.docx', '.txt', '.pptx'],
    'videos': ['.mp4', '.mkv', '.avi'],
    'music': ['.mp3', '.wav', '.flac'],
    'archives': ['.zip', '.rar', '.tar'],
}