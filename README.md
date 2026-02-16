# 🤖 Polymarket Telegram Tracker

Polymarket pozisyonlarınızı otomatik takip eden Telegram botu. **Tamamen ücretsiz!**

## ✨ Özellikler

- ⚡ **10 saniyede bir tarama** - Hiçbir fırsatı kaçırmayın
- 🚨 **%150+ spike alertleri** - Anormal fiyat hareketlerinde ANINDA bildirim
- 📊 **5 dakikada periyodik raporlar** - Düzenli pozisyon özeti
- 💰 **Gerçek zamanlı kar/zarar** - Anlık P&L hesaplama
- 🔄 **7/24 arka plan çalışma** - Bilgisayarınız açıkken sürekli aktif
- 🆓 **Tamamen ücretsiz** - Sadece public Polymarket API

---

## 🚀 Hızlı Kurulum (5 Dakika)

### Gereksinimler
- Ubuntu/Linux (Windows WSL de çalışır)
- Python 3.7+
- Polymarket hesabı
- Telegram hesabı

### Adım 1: Telegram Bot Oluştur

1. Telegram'da [@BotFather](https://t.me/BotFather) ile konuş
2. `/newbot` komutunu gönder
3. Bot adı belirle (örn: "My Polymarket Tracker")
4. Kullanıcı adı belirle (örn: "my_polymarket_bot") - "bot" ile bitmeli
5. **TOKEN**'ı kaydet (örn: `1234567890:ABCdefGHI...`)

### Adım 2: Chat ID Bul

1. [@userinfobot](https://t.me/userinfobot) ile konuş
2. Herhangi bir mesaj gönder
3. **ID numaranı** kaydet (örn: `987654321`)

### Adım 3: Wallet Adresi

Polymarket profilinizden (sağ üstteki profil resmi) wallet adresinizi kopyalayın.
- `0x` ile başlamalı
- 42 karakter uzunluğunda

### Adım 4: Dosyaları İndir ve Kur

```bash
# Repo'yu klonla veya dosyaları indir
git clone https://github.com/sooneraydin/polymarket-telegram-tracker.git
cd polymarket-telegram-tracker

# Kurulum scriptini çalıştır
chmod +x setup.sh
./setup.sh
```

### Adım 5: Ayarları Yap

```bash
# .env dosyasını düzenle
nano .env.telegram
```

Şu değerleri değiştir:
```bash
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=987654321
POLYMARKET_ADDRESS=0x1234567890abcdef1234567890abcdef12345678
```

Kaydet: `Ctrl + X` → `Y` → `Enter`

### Adım 6: Bot'u Başlat

```bash
python3 telegram_tracker.py
```

✅ **Telegram'dan mesaj gelirse başarılı!**

---

## 📱 Örnek Bildirimler

### 🚨 Spike Alert (Anında)
```
🚨 AŞIRI FİYAT ARTIŞI ALGILANDI! 🚨

⚡ %165.4 YUKARI HAREKET!

❓ Will BTC be above $95,000...

💥 Fiyat Değişimi:
   Önceki: $0.420
   Şimdi: $1.115
   Değişim: +$0.695 (+165.4%)

🟢 P&L Etkisi:
   Nakit: +$34.75
   Yüzde: +165.4%

💡 Öneri: Kar realizasyonu düşünün!
```

### 📊 Periyodik Rapor (5 Dakika)
```
📊 POLYMARKET POZİSYONLAR
🕐 2026-02-16 14:30 UTC

🟢 Pozisyon #1
❓ Will BTC be above $95,000...
📍 Yes
📈 Giriş: $0.650 | Şimdi: $0.720
💼 Miktar: 50.0 shares
💰 P&L: +$3.50 (+10.8%)

────────────────────────────────
🟢 TOPLAM P&L: +$3.50
```

---

## 🔧 İleri Seviye

### Arka Planda Çalıştırma (Systemd)

Bot'u bilgisayar kapanana kadar arka planda çalıştır:

```bash
chmod +x systemd_install.sh
./systemd_install.sh
```

Kontrol komutları:
```bash
# Durum
sudo systemctl status polymarket-tracker

# Loglar
sudo journalctl -u polymarket-tracker -f

# Durdur/Başlat
sudo systemctl stop polymarket-tracker
sudo systemctl start polymarket-tracker
```

### Ayarları Özelleştir

`telegram_tracker.py` dosyasının başındaki değerleri değiştir:

```python
CHECK_INTERVAL = 10        # Tarama hızı (saniye)
REPORT_INTERVAL = 300      # Rapor sıklığı (saniye)
SPIKE_ALERT_THRESHOLD = 150 # Alert eşiği (%)
```

---

## 🐛 Sorun Giderme

### "Telegram credentials eksik"
```bash
# .env dosyasını kontrol et
cat .env.telegram

# Düzenle
nano .env.telegram
```

### "Pozisyon bulunamadı"
1. Wallet adresinizi kontrol edin
2. Polymarket'te aktif pozisyonunuz var mı?
3. 2-3 dakika bekleyip tekrar deneyin

### Telegram'dan mesaj gelmiyor
```bash
# Bot çalışıyor mu?
ps aux | grep telegram_tracker

# Logları kontrol et
tail -f /var/log/syslog | grep telegram
```

---

## 🔒 Güvenlik

✅ **Bot tamamen güvenli:**
- Sadece OKUMA yapıyor (trade yapmıyor)
- Private key gerektirmiyor
- Sadece public API kullanıyor

❌ **ASLA:**
- Private key'inizi paylaşmayın
- Bot token'ınızı GitHub'a yüklemeyin
- `.env.telegram` dosyasını public yapmayın

---

## ⚙️ Teknik Detaylar

| Özellik | Değer |
|---------|-------|
| Tarama Sıklığı | 10 saniye |
| Rapor Sıklığı | 5 dakika |
| Spike Alert | %150+ |
| API Kullanımı | ~400 request/saat |
| Veri Kullanımı | ~1-2 MB/saat |
| CPU Kullanımı | <1% |
| RAM Kullanımı | ~50 MB |

**API Endpoint:** `https://data-api.polymarket.com/positions?user=WALLET`

---

## 📝 Lisans

MIT License - Özgürce kullanabilirsiniz!

---

## 🤝 Katkıda Bulunma

Pull request'ler hoş karşılanır!

1. Fork'layın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit'leyin (`git commit -m 'Add amazing feature'`)
4. Push'layın (`git push origin feature/amazing-feature`)
5. Pull Request açın

---

## 💡 İpuçları

- İlk 24 saat varsayılan ayarlarla test edin
- %150 spike alert çok hassassa, %200'e çıkarın
- Daha sık rapor istiyorsanız REPORT_INTERVAL'i 180'e indirin (3 dakika)
- Batarya tasarrufu için CHECK_INTERVAL'i 30'a çıkarın

---

## 📞 Destek

Sorunlarınız için:
1. [Issues](https://github.com/sooneraydin/polymarket-telegram-tracker/issues) bölümüne bakın
2. Yeni issue açın
3. README'yi tekrar okuyun

---

## 🎯 Yol Haritası

- [ ] Web dashboard
- [ ] Birden fazla wallet takibi
- [ ] Discord entegrasyonu
- [ ] SMS alertleri
- [ ] Özel alert kuralları

---

**⭐ Beğendiyseniz GitHub'da yıldız vermeyi unutmayın!**

🚀 **Mutlu kazançlar!**
