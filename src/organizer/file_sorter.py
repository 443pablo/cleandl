import os
import shutil
from pathlib import Path

class FileSorter:
    def __init__(self, file_mappings):
        self.file_mappings = file_mappings
        self.organized_root = "Organized"
    
    def sort_files(self, downloads_folder):
        downloads_path = Path(downloads_folder)
        organized_path = downloads_path / self.organized_root
        
        self._create_category_folders(organized_path)
        
        for file_path in downloads_path.iterdir():
            if file_path.is_file() and file_path.name != self.organized_root:
                self._create_hardlink_for_file(file_path, organized_path)
    
    def _create_category_folders(self, organized_path):
        for category in self.file_mappings.keys():
            category_path = organized_path / category
            category_path.mkdir(parents=True, exist_ok=True)
    
    def _create_hardlink_for_file(self, file_path, organized_path):
        file_extension = file_path.suffix.lower()
        category = self._get_category_for_extension(file_extension)
        
        if category:
            target_folder = organized_path / category
            link_path = target_folder / file_path.name
            
            if link_path.exists():
                link_path.unlink()
            
            try:
                link_path.hardlink_to(file_path)
                print(f"Created hardlink: {file_path.name} -> {category}")
            except OSError as e:
                try:
                    import shutil
                    shutil.copy2(file_path, link_path)
                    print(f"Copied (hardlink failed): {file_path.name} -> {category}")
                except Exception as copy_error:
                    print(f"Could not create link for {file_path.name}: {e}")
    
    def _get_category_for_extension(self, extension):
        for category, extensions in self.file_mappings.items():
            if extension in extensions:
                return category
    
    def cleanup_broken_symlinks(self, downloads_folder):
        downloads_path = Path(downloads_folder)
        organized_path = downloads_path / self.organized_root
        
        if not organized_path.exists():
            return
        
        removed_count = 0
        for category_folder in organized_path.iterdir():
            if category_folder.is_dir():
                for link_file in category_folder.iterdir():
                    if link_file.is_file():
                        original_file = downloads_path / link_file.name
                        if not original_file.exists():
                            link_file.unlink()
                            removed_count += 1
        
        print(f"Removed {removed_count} broken links")
    
    def delete_organized_directory(self, downloads_folder):
        downloads_path = Path(downloads_folder)
        organized_path = downloads_path / self.organized_root
        
        if organized_path.exists():
            shutil.rmtree(organized_path)
            print(f"Deleted organized directory: {organized_path}")
            return True
        else:
            print("Organized directory not found")
            return False