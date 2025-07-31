import os
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import json
from datetime import datetime

from organizer.file_sorter import FileSorter
from organizer.scheduler import Scheduler
from organizer.memory_optimizer import MemoryOptimizer
from config.file_mappings import file_mappings
from utils.logger import log_info, log_error, log_warning

class DownloadsOrganizer:
    def __init__(self):
        self.file_sorter = FileSorter(file_mappings)
        self.scheduler = Scheduler()
        self.memory_optimizer = MemoryOptimizer()

        self.downloads_folder = os.path.expanduser("~/Downloads")

    def start(self):
        log_info("cleanDL started")
        self.scheduler.schedule_daily_cleanup()
        self.auto_sort_files()

    def auto_sort_files(self):
        while True:
            self.file_sorter.sort_files(self.downloads_folder)
            self.memory_optimizer.optimize_memory()
            time.sleep(3600)

class DownloadOrganizerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("cleanDL")
        self.root.geometry("600x350")
        
        self.file_sorter = FileSorter(file_mappings)
        self.memory_optimizer = MemoryOptimizer()
        
        self.downloads_folder = os.path.expanduser("~/Downloads")

        self.setup_ui()

    def setup_ui(self):
        folder_frame = ttk.Frame(self.root, padding="10")
        folder_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

        ttk.Label(folder_frame, text="Downloads Folder:").grid(row=0, column=0, sticky=tk.W)
        self.folder_var = tk.StringVar(value=self.downloads_folder)
        ttk.Entry(folder_frame, textvariable=self.folder_var, width=40).grid(row=1, column=0, padx=(0,5))
        ttk.Button(folder_frame, text="Browse", command=self.browse_folder).grid(row=1, column=1)

        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.grid(row=1, column=0, pady=10)
        
        ttk.Button(button_frame, text="Create Organized View", command=self.manual_cleanup).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Cleanup Broken Links", command=self.cleanup_hardlinks).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Delete Organized Directory", command=self.delete_organized).grid(row=0, column=2, padx=5)

        info_text = tk.Text(self.root, height=8, width=60, wrap=tk.WORD)
        info_text.grid(row=2, column=0, padx=10, pady=10)
        info_text.insert(tk.END, 
            "cleanDL:\n"
            "• creates an 'Organized' folder in your downloads\n"
            "• files stay in original location\n"
            "• organized view shows files sorted by type\n"
            "• categories: Documents, Images, Videos, Music, Archives\n"
            "• original files remain untouched\n"
            "• uses hardlinks, doesnt duplicate files")
        info_text.config(state=tk.DISABLED)

        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(self.root, textvariable=self.status_var).grid(row=3, column=0, pady=10)

    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.downloads_folder)
        if folder:
            self.folder_var.set(folder)
            self.downloads_folder = folder

    def manual_cleanup(self):
        self.downloads_folder = self.folder_var.get()
        self.status_var.set("Creating organized hardlink structure...")
        threading.Thread(target=self._organize_files, daemon=True).start()
    
    def cleanup_hardlinks(self):
        self.downloads_folder = self.folder_var.get()
        self.status_var.set("Cleaning up broken hardlinks...")
        threading.Thread(target=self._cleanup_broken_links, daemon=True).start()

    def delete_organized(self):
        # confirm deletion with user
        result = messagebox.askyesno(
            "Confirm Deletion", 
            "Are you sure you want to delete the entire Organized directory?\n\nThis will remove all organized files (but original files will remain untouched)."
        )
        if result:
            self.downloads_folder = self.folder_var.get()
            self.status_var.set("Deleting organized directory...")
            threading.Thread(target=self._delete_organized_directory, daemon=True).start()

    def _organize_files(self):
        try:
            self.file_sorter.sort_files(self.downloads_folder)
            self.root.after(0, lambda: self.status_var.set("Organized view created successfully!"))
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"Error: {str(e)}"))
    
    def _cleanup_broken_links(self):
        try:
            self.file_sorter.cleanup_broken_symlinks(self.downloads_folder)
            self.root.after(0, lambda: self.status_var.set("Broken hardlinks cleaned up!"))
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"Error: {str(e)}"))

    def _delete_organized_directory(self):
        try:
            success = self.file_sorter.delete_organized_directory(self.downloads_folder)
            if success:
                self.root.after(0, lambda: self.status_var.set("Organized directory deleted successfully!"))
            else:
                self.root.after(0, lambda: self.status_var.set("Organized directory not found"))
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"Error: {str(e)}"))

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = DownloadOrganizerApp()
    app.run()