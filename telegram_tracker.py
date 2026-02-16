"""
Polymarket Position Tracker - Telegram Bot v4.0 FINAL
Data API kullanan çalışan versiyon
"""
import os
import json
import time
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

# ══════════════════════════════════════════════════
# CONFIGURATION
# ══════════════════════════════════════════════════
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
POLYMARKET_ADDRESS = os.getenv("POLYMARKET_ADDRESS", "")

# Tarama ayarları
CHECK_INTERVAL = 10  # Her 10 saniyede kontrol
REPORT_INTERVAL = 300  # Her 5 dakikada rapor (300 saniye)

# Alert eşikleri
SPIKE_ALERT_THRESHOLD = 150  # %150+ artışta anında alert
NORMAL_CHANGE_THRESHOLD = 2  # Normal değişim takibi

# API - ÇALIŞAN ENDPOINT
DATA_API = "https://data-api.polymarket.com"

# Dosyalar
POSITIONS_FILE = "telegram_positions.json"
LAST_REPORT_FILE = "last_report_time.json"


# ══════════════════════════════════════════════════
# TELEGRAM FUNCTIONS
# ══════════════════════════════════════════════════
def send_telegram(message):
    """Telegram'a mesaj gönder"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️  Telegram credentials eksik!")
        return False
    
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }
        r = requests.post(url, data=data, timeout=10)
        return r.status_code == 200
    except Exception as e:
        print(f"❌ Telegram hatası: {e}")
        return False


# ══════════════════════════════════════════════════
# POLYMARKET DATA API - ÇALIŞAN VERSİYON
# ══════════════════════════════════════════════════
def get_positions():
    """Data API'den pozisyonları çek - ÇALIŞIYOR!"""
    if not POLYMARKET_ADDRESS:
        return []
    
    try:
        url = f"{DATA_API}/positions"
        params = {"user": POLYMARKET_ADDRESS}
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        }
        
        r = requests.get(url, params=params, headers=headers, timeout=15)
        
        if r.status_code != 200:
            print(f"⚠️ API error: {r.status_code}")
            return []
        
        positions = r.json()
        
        # Sadece size > 0 olanları al
        active_positions = []
        for pos in positions:
            size = float(pos.get("size", 0))
            if size > 0:
                active_positions.append({
                    "asset": pos.get("asset"),
                    "title": pos.get("title", "Unknown"),
                    "outcome": pos.get("outcome", "Unknown"),
                    "size": size,
                    "avgPrice": float(pos.get("avgPrice", 0)),
                    "curPrice": float(pos.get("curPrice", 0)),
                    "initialValue": float(pos.get("initialValue", 0)),
                    "currentValue": float(pos.get("currentValue", 0)),
                    "cashPnl": float(pos.get("cashPnl", 0)),
                    "percentPnl": float(pos.get("percentPnl", 0)),
                    "endDate": pos.get("endDate", ""),
                })
        
        return active_positions
        
    except Exception as e:
        print(f"❌ API hatası: {e}")
        return []


# ══════════════════════════════════════════════════
# SPIKE DETECTION
# ══════════════════════════════════════════════════
def format_spike_alert(pos, old_price, new_price):
    """Spike alert mesajı"""
    price_change = new_price - old_price
    price_change_pct = (price_change / old_price * 100) if old_price > 0 else 0
    
    lines = ["🚨 <b>AŞIRI FİYAT ARTIŞI ALGILANDI!</b> 🚨\n"]
    lines.append(f"⚡ <b>%{abs(price_change_pct):.1f} {'YUKARI' if price_change > 0 else 'AŞAĞI'} HAREKET!</b>\n")
    lines.append(f"❓ {pos['title'][:70]}...")
    lines.append(f"📍 <b>{pos['outcome']}</b> pozisyonu")
    lines.append(f"\n💥 <b>Fiyat Değişimi:</b>")
    lines.append(f"   Önceki: ${old_price:.3f}")
    lines.append(f"   Şimdi: ${new_price:.3f}")
    lines.append(f"   Değişim: ${price_change:+.3f} ({price_change_pct:+.1f}%)")
    
    pnl_emoji = "🟢" if pos["cashPnl"] > 0 else "🔴"
    lines.append(f"\n{pnl_emoji} <b>P&L Durumu:</b>")
    lines.append(f"   Nakit: ${pos['cashPnl']:+.2f}")
    lines.append(f"   Yüzde: {pos['percentPnl']:+.1f}%")
    lines.append(f"   Değer: ${pos['currentValue']:.2f}")
    
    if price_change_pct > SPIKE_ALERT_THRESHOLD:
        lines.append(f"\n💡 <b>Öneri:</b> Kar realizasyonu düşünün!")
    elif price_change_pct < -SPIKE_ALERT_THRESHOLD:
        lines.append(f"\n⚠️ <b>Uyarı:</b> Pozisyonu gözden geçirin!")
    
    lines.append(f"\n⏰ {datetime.now(timezone.utc).strftime('%H:%M:%S UTC')}")
    
    return "\n".join(lines)


def should_send_report(last_report_time):
    """Rapor zamanı kontrolü"""
    if last_report_time is None:
        return True
    elapsed = (datetime.now(timezone.utc) - last_report_time).total_seconds()
    return elapsed >= REPORT_INTERVAL


def load_last_report_time():
    """Son rapor zamanını yükle"""
    if os.path.exists(LAST_REPORT_FILE):
        try:
            with open(LAST_REPORT_FILE, "r") as f:
                data = json.load(f)
                return datetime.fromisoformat(data.get("last_report"))
        except:
            return None
    return None


def save_last_report_time():
    """Son rapor zamanını kaydet"""
    try:
        with open(LAST_REPORT_FILE, "w") as f:
            json.dump({"last_report": datetime.now(timezone.utc).isoformat()}, f)
    except:
        pass


def load_tracked_positions():
    """Tracked positions"""
    if os.path.exists(POSITIONS_FILE):
        try:
            with open(POSITIONS_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_tracked_positions(positions):
    """Tracked positions kaydet"""
    try:
        with open(POSITIONS_FILE, "w") as f:
            json.dump(positions, f, indent=2)
    except:
        pass


# ══════════════════════════════════════════════════
# REPORTING
# ══════════════════════════════════════════════════
def format_position_report(positions):
    """Pozisyon raporu - Data API formatında"""
    if not positions:
        return "📊 <b>Açık Pozisyon Yok</b>"
    
    total_pnl = sum(p["cashPnl"] for p in positions)
    total_value = sum(p["currentValue"] for p in positions)
    
    lines = ["📊 <b>POLYMARKET POZİSYONLAR</b>\n"]
    lines.append(f"🕐 {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\n")
    
    for i, pos in enumerate(positions, 1):
        # Emoji kar/zarar
        emoji = "🟢" if pos["cashPnl"] > 0 else "🔴" if pos["cashPnl"] < 0 else "⚪"
        
        lines.append(f"\n{emoji} <b>Pozisyon #{i}</b>")
        lines.append(f"❓ {pos['title'][:65]}...")
        lines.append(f"📍 <b>{pos['outcome']}</b>")
        lines.append(f"📈 Giriş: ${pos['avgPrice']:.3f} | Şimdi: ${pos['curPrice']:.3f}")
        lines.append(f"💼 Miktar: {pos['size']:.1f} shares")
        lines.append(f"💰 P&L: ${pos['cashPnl']:+.2f} ({pos['percentPnl']:+.1f}%)")
        lines.append(f"💵 Değer: ${pos['initialValue']:.2f} → ${pos['currentValue']:.2f}")
    
    # Toplam
    lines.append("\n" + "─" * 40)
    total_emoji = "🟢" if total_pnl > 0 else "🔴" if total_pnl < 0 else "⚪"
    lines.append(f"\n{total_emoji} <b>TOPLAM</b>")
    lines.append(f"💰 Toplam P&L: ${total_pnl:+.2f}")
    lines.append(f"💵 Toplam Değer: ${total_value:.2f}")
    
    return "\n".join(lines)


# ══════════════════════════════════════════════════
# MAIN LOOP
# ══════════════════════════════════════════════════
def check_and_report():
    """Ana kontrol döngüsü"""
    now_str = datetime.now(timezone.utc).strftime('%H:%M:%S')
    print(f"🔍 Kontrol... {now_str}", end=" ")
    
    # Pozisyonları çek
    positions = get_positions()
    
    if not positions:
        print("→ Pozisyon yok")
        return
    
    print(f"→ {len(positions)} pozisyon", end="")
    
    # Tracked positions yükle
    tracked = load_tracked_positions()
    
    spike_detected = False
    changes_detected = False
    
    # Her pozisyonu kontrol et
    for pos in positions:
        asset = pos["asset"]
        if not asset:
            continue
        
        current_price = pos["curPrice"]
        
        # Önceki fiyatı kontrol et
        if asset in tracked:
            old_pos = tracked[asset]
            old_price = old_pos.get("last_price", pos["avgPrice"])
            
            # Fiyat değişimi hesapla
            if old_price > 0:
                price_change_pct = abs((current_price - old_price) / old_price * 100)
                
                # 🚨 SPIKE DETECTION
                if price_change_pct >= SPIKE_ALERT_THRESHOLD:
                    alert = format_spike_alert(pos, old_price, current_price)
                    if send_telegram(alert):
                        print(f"\n   🚨 SPIKE ALERT! {price_change_pct:.1f}%", end="")
                        spike_detected = True
                
                # Normal değişim
                elif price_change_pct >= NORMAL_CHANGE_THRESHOLD:
                    changes_detected = True
        
        # Güncelle
        tracked[asset] = {
            "title": pos["title"],
            "last_price": current_price,
            "last_pnl": pos["cashPnl"],
            "last_check": datetime.now(timezone.utc).isoformat(),
        }
    
    # Kaydı güncelle
    save_tracked_positions(tracked)
    
    # 📊 Periyodik rapor
    last_report_time = load_last_report_time()
    if should_send_report(last_report_time):
        report = format_position_report(positions)
        if send_telegram(report):
            save_last_report_time()
            print("\n   ✅ Periyodik rapor gönderildi", end="")
    elif spike_detected:
        pass  # Spike zaten gönderildi
    elif changes_detected:
        print("\n   ℹ️  Değişim var, rapor zamanı bekleniyor", end="")
    
    print()  # Newline


def main():
    """Ana fonksiyon"""
    print("=" * 60)
    print("🤖 POLYMARKET TELEGRAM TRACKER v4.0 FINAL")
    print("=" * 60)
    
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("\n❌ HATA: Telegram bilgileri eksik!")
        print("Lütfen .env.telegram dosyasını kontrol edin")
        return
    
    if not POLYMARKET_ADDRESS:
        print("\n❌ HATA: Polymarket adresi eksik!")
        return
    
    print(f"\n✅ Bot başlatıldı")
    print(f"📍 Adres: {POLYMARKET_ADDRESS[:10]}...{POLYMARKET_ADDRESS[-6:]}")
    print(f"⚡ Tarama: Her {CHECK_INTERVAL} saniye")
    print(f"📊 Rapor: Her {REPORT_INTERVAL//60} dakika")
    print(f"🚨 Spike Alert: %{SPIKE_ALERT_THRESHOLD}+")
    print()
    
    # Başlangıç bildirimi
    startup_msg = f"""
🤖 <b>Tracker v4.0 Başlatıldı</b>

✅ Data API entegrasyonu ÇALIŞIYOR
⚡ {CHECK_INTERVAL} saniyede tarama
📊 {REPORT_INTERVAL//60} dakikada rapor
🚨 %{SPIKE_ALERT_THRESHOLD}+ spike alert!

Pozisyonlarınız takip ediliyor 👀
    """.strip()
    send_telegram(startup_msg)
    
    # İlk pozisyon kontrolü
    time.sleep(2)
    positions = get_positions()
    
    if positions:
        report = format_position_report(positions)
        send_telegram(report)
        save_last_report_time()
        print(f"📊 İlk rapor gönderildi: {len(positions)} pozisyon\n")
    else:
        msg = "⚠️ Henüz açık pozisyon bulunamadı."
        send_telegram(msg)
        print("⚠️ Pozisyon yok\n")
    
    # Ana döngü
    try:
        check_count = 0
        while True:
            try:
                check_count += 1
                check_and_report()
                
                # Her 60 kontrol (10 dakika) istatistik
                if check_count % 60 == 0:
                    elapsed_min = (check_count * CHECK_INTERVAL) // 60
                    print(f"\n📈 {check_count} kontrol tamamlandı ({elapsed_min} dakika)\n")
                
            except Exception as e:
                print(f"❌ Döngü hatası: {e}")
            
            time.sleep(CHECK_INTERVAL)
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Bot durduruldu")
        send_telegram("⏹️ <b>Tracker Durduruldu</b>")


if __name__ == "__main__":
    main()
