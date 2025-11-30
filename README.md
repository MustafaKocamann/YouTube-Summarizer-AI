# 📺 YouTube Summarizer AI  
### Professional Video Transcript Analyzer & LLM-Powered Summarizer

YouTube Summarizer AI, YouTube videolarının altyazılarını otomatik olarak alıp **Google Gemini 2.5 Flash** modeli ile profesyonel, yapılandırılmış özetler üreten modern bir Streamlit uygulamasıdır.

Bu proje; YouTube Transcript API, gelişmiş Prompt Engineering ve LLM tabanlı metin işleme tekniklerini birleştirerek kullanıcıya **hızlı, güvenilir ve yüksek kaliteli** özetleme deneyimi sunar.

---

## 🚀 Özellikler

- 🔍 **Otomatik YouTube Video ID Algılama**  
  Kullanıcıdan alınan bağlantıyı işleyerek video ID’sini otomatik çıkarır.

- 📝 **Transcript (Altyazı) Alma**  
  YouTube Transcript API ile videonun altyazısını çeker  
  _(altyazı yoksa veya IP engelliyse anlamlı bir hata mesajı döner)._

- 🤖 **Gemini 2.5 Flash ile Özetleme**  
  Gelişmiş özetleme için özel olarak hazırlanmış profesyonel sistem promptu kullanılır.

- 🧠 **ZERO-HALLUCINATION POLICY**  
  Model yalnızca verilen transcript içeriğine dayanarak özet oluşturur.

- 🎨 **Modern Streamlit Arayüzü**  
  Basit, zarif ve kullanıcı dostu tasarım.

- 🛡️ **Sağlam Hata Yönetimi**  
  - Altyazı yoksa  
  - IP YouTube tarafından bloklanmışsa  
  - Yanlış link verilmişse  
  Anlaşılır uyarılar gösterir.

---

## 🧪 Kullanım
* YouTube video bağlantısını yapıştır
* Önizleme olarak video thumbnail'i gelir
* Generate Summary 🚀 butonuna tıkla
* Transcript çekilir → Gemini modele gönderilir
* Yapılandırılmış Markdown özet ekranda gösterilir

## ⚠️ Önemli Notlar
* Bazı videolarda altyazı yoktur → özet üretilemez
* Çok fazla istek atan IP adresleri YouTube tarafından geçici olarak engellenebilir
→ Bu durumda uygulama özel bir hata mesajı verir
* Cloud/VPN IP’leri YouTube tarafından daha sık bloklanır

## 📦 Kullanılan Teknolojiler
* Python 3.10+
* Streamlit
* youtube-transcript-api
* Google Gemini 2.5 Flash
* dotenv
* Modern Prompt Engineering

