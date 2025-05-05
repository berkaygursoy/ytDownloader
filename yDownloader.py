import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import yt_dlp
import os


class YTDLPDownloader:
        def __init__(self, root):
            self.root = root
            self.root.title("YouTube Video İndirici (yt-dlp)")
            self.root.geometry("550x350")
            self.root.resizable(False, False)

            self.url_var = tk.StringVar()
            self.formats = []

            self.create_widgets()

        def create_widgets(self):
            tk.Label(self.root, text="YouTube Video URL'si:", font=("Arial", 12)).pack(
                pady=10
            )
            tk.Entry(self.root, textvariable=self.url_var, width=70).pack(pady=5)

            tk.Button(self.root, text="Formatları Getir", command=self.fetch_formats).pack(
                pady=10
            )

            self.format_combo = ttk.Combobox(self.root, state="readonly", width=68)
            self.format_combo.pack(pady=10)
            self.progress = ttk.Progressbar(
                self.root, orient="horizontal", length=400, mode="determinate"
            )
            self.progress.pack(pady=10)

            tk.Button(self.root, text="İndir", command=self.download_video).pack(pady=10)

        def fetch_formats(self):
            url = self.url_var.get().strip()
            if not url.startswith(("http://", "https://")):
                messagebox.showwarning("Uyarı", "Lütfen geçerli bir URL girin.")
                return

            ydl_opts = {"quiet": True, "skip_download": True}
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)

                # Filter for formats with both video and audio
                self.formats = [
                    f
                    for f in info["formats"]
                    if f.get("vcodec") != "none" and f.get("acodec") != "none"
                ]
                if not self.formats:
                    raise Exception("Uygun format bulunamadı.")

                # Prepare display list
                display_list = []
                for f in self.formats:
                    res = (
                        f.get("resolution")
                        or f.get("height")
                        and f"{f['height']}p"
                        or "unknown"
                    )
                    size_mb = f.get("filesize") or f.get("filesize_approx") or 0
                    size_mb = round(size_mb / (1024 * 1024), 2)
                    display_list.append(f"{f['format_id']} - {res} - {size_mb} MB")

                self.format_combo["values"] = display_list
                self.format_combo.current(0)
                messagebox.showinfo("Başarılı", "Format bilgileri alındı.")
            except Exception as e:
                messagebox.showerror("Hata", f"Formatlar alınamadı:\n{e}")

        def download_video(self):
            if not self.formats:
                messagebox.showwarning("Uyarı", "Lütfen önce format bilgilerini alın.")
                return

            idx = self.format_combo.current()
            if idx == -1:
                messagebox.showwarning("Uyarı", "Lütfen bir format seçin.")
                return

            save_dir = filedialog.askdirectory(title="İndirme klasörünü seçiniz:")
            if not save_dir:
                return

            selected_format = self.formats[idx]['format_id']
            url = self.url_var.get().strip()

            def run_download():
                def progress_hook(d):
                    if d['status'] == 'downloading':
                        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
                        downloaded = d.get('downloaded_bytes', 0)
                        if total_bytes:
                            percent = downloaded / total_bytes * 100
                            self.progress["value"] = percent
                            self.root.update_idletasks()
                    elif d['status'] == 'finished':
                        self.progress["value"] = 100
                        self.root.update_idletasks()

                ydl_opts = {
                    'format': selected_format,
                    'outtmpl': os.path.join(save_dir, '%(title)s.%(ext)s'),
                    'noplaylist': True,
                    'progress_hooks': [progress_hook],
                    'quiet': True
                }

                try:
                    self.progress["value"] = 0
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
                    messagebox.showinfo("Başarılı", "Video başarıyla indirildi!")
                except Exception as e:
                    messagebox.showerror("Hata", f"İndirme sırasında hata oluştu:\n{e}")
                    self.progress["value"] = 0

            # Arka planda çalıştır
            threading.Thread(target=run_download, daemon=True).start()


if __name__ == "__main__":
    root = tk.Tk()
    app = YTDLPDownloader(root)
    root.mainloop()
