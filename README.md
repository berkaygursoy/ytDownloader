# ytDownloader
Python ve yt-dlp kullanarak video çözünürlüğü seçimiyle YouTube indirme işlemi yapan bir masaüstü uygulaması yaptım.

# YouTube Video İndirici (yt-dlp + Tkinter)

Bu proje, Python ile geliştirilmiş basit bir masaüstü YouTube video indiricisidir.  
Kullanıcı, video bağlantısını girip çözünürlük/format seçerek istediği klasöre kolayca indirme yapabilir.

## Özellikler
- Basit ve anlaşılır arayüz (Tkinter)
- YouTube video URL'si ile çalışma
- Video formatı ve çözünürlüğü seçme
- İlerleme çubuğu ile indirme durumu gösterme
- Arayüz donmadan çalışan indirme (thread desteği)
- `yt-dlp` altyapısı sayesinde stabil indirme

## Gereksinimler
- Python 3.7+
- `yt-dlp` kütüphanesi:
