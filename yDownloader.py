import yt_dlp
import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


def quit():
    root.destroy()


def download_video():
    url = url_entry.get().strip()
    if not url:
        messagebox.showwarning("Lütfen bir YouTube Url'si giriniz: ")
        return

    save_dir = filedialog.askdirectory(title="İndirilecek yeri seçiniz: ")
    if not save_dir:
        messagebox.showerror("Hata" "Lütfen geçerli bir dizin seçiniz.")
        return

    def run():
        def progress_hook(d):
            if d["status"] == "downloading":
                total = d.get("total_bytes") or d.get("total_bytes_esimate")
                downloaded = d.get("downloaded_bytes", 0)
                if total:
                    percent = downloaded / total * 100
                    progress["value"] = percent
                    root.update_idletasks()
            elif d["status"] == "finished":
                progress["value"] = 100
                root.update_idletasks()

        selected_format = format_combo.get()

        ydl_opts = {
            "format": "best",
            "outtmpl": os.path.join(save_dir, "%(title)s.%(ext)s"),
            "quiet": True,
            "progress_hooks": [progress_hook],
        }

        if selected_format == "MP3":
            ydl_opts.update(
                {
                    "format": "bestaudio/best",
                    "postprocessors": [
                        {
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": "mp3",
                            "preferredquality": "192",
                        }
                    ],
                }
            )
        else:
            format_map = {
                "En İyi Kalite": "best",
                "MP4": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                "WebM": "bestvideo[ext=webm]+bestaudio[ext=webm]/best[ext=webm]/best",
            }
            ydl_opts["format"] = format_map.get(selected_format, "best")

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            messagebox.showinfo("Başarılı", "İndirme tamamlandı.")
        except Exception as e:
            messagebox.showerror("Hata", f"İndirme başarısız:\n{e}")

    threading.Thread(target=run, daemon=True).start()


root = tk.Tk()
root.title("Youtube Video İndirici")
root.geometry("500x200")
root.resizable(False, False)

tk.Label(root, text="YouTube URL'si giriniz:", font=("Arial", 12)).pack(pady=5)
url_entry = tk.Entry(root, width=60)
url_entry.pack(pady=5)

tk.Label(root, text="İndirme Formatını Seçin:", font=("Arial", 12)).pack(pady=5)
format_combo = ttk.Combobox(
    root, values=["En İyi Kalite", "MP4", "WebM", "MP3"], state="readonly"
)
format_combo.current(0)
format_combo.pack()

progress = ttk.Progressbar(root, orient="horizontal", length=365, mode="determinate")
progress.pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack(pady=5)
tk.Button(button_frame, text="İndir", command=download_video, font=("Arial", 12)).pack(
    side=tk.LEFT, padx=10
)
tk.Button(button_frame, text="Çıkış", command=quit, font=("Arial", 12)).pack(
    side=tk.LEFT, padx=10
)

root.mainloop()
