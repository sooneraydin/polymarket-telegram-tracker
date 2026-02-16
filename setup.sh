#!/bin/bash

echo "=========================================="
echo "🚀 Polymarket Telegram Tracker - Kurulum"
echo "=========================================="
echo ""

# Renk kodları
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Python kontrolü
echo -e "${BLUE}📦 Bağımlılıklar kontrol ediliyor...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 bulunamadı!${NC}"
    echo -e "${YELLOW}Yükleniyor...${NC}"
    sudo apt update
    sudo apt install python3 python3-pip -y
fi

echo -e "${GREEN}✅ Python3: $(python3 --version)${NC}"
echo ""

# Pip kontrolü
if ! command -v pip3 &> /dev/null; then
    echo -e "${YELLOW}📦 Pip yükleniyor...${NC}"
    sudo apt install python3-pip -y
fi

# Gerekli kütüphaneleri yükle
echo -e "${BLUE}📦 Python kütüphaneleri yükleniyor...${NC}"
pip3 install python-dotenv requests --quiet

echo -e "${GREEN}✅ Kütüphaneler yüklendi${NC}"
echo ""

# .env dosyası kontrolü
if [ ! -f ".env.telegram" ]; then
    echo -e "${YELLOW}⚠️  .env.telegram dosyası bulunamadı!${NC}"
    echo -e "${BLUE}📝 Şablon oluşturuluyor...${NC}"
    cat > .env.telegram << 'EOF'
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
POLYMARKET_ADDRESS=your_wallet_address_here
EOF
    echo -e "${GREEN}✅ .env.telegram şablonu oluşturuldu${NC}"
    echo -e "${YELLOW}⚠️  Lütfen .env.telegram dosyasını düzenleyin!${NC}"
    echo ""
fi

# Telegram bot dosyası kontrolü
if [ ! -f "telegram_tracker.py" ]; then
    echo -e "${RED}❌ telegram_tracker.py dosyası bulunamadı!${NC}"
    echo -e "${YELLOW}Bu dosyayı indirilen paket içinden buraya kopyalayın.${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✅ Kurulum tamamlandı!${NC}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}📋 YAPMANZ GEREKENLER:${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${YELLOW}1️⃣  Telegram Bot Oluştur${NC}"
echo "   • @BotFather ile konuş → /newbot"
echo "   • Token'ı kaydet"
echo ""
echo -e "${YELLOW}2️⃣  Chat ID Bul${NC}"
echo "   • @userinfobot ile konuş"
echo "   • ID'ni kaydet"
echo ""
echo -e "${YELLOW}3️⃣  Wallet Adresini Bul${NC}"
echo "   • https://polymarket.com/@Sooneraydin"
echo "   • Profilde görünen 0x ile başlayan adresi kopyala"
echo ""
echo -e "${YELLOW}4️⃣  .env.telegram dosyasını düzenle${NC}"
echo "   nano .env.telegram"
echo ""
echo -e "${YELLOW}5️⃣  Botu başlat${NC}"
echo "   python3 telegram_tracker.py"
echo ""
echo -e "${YELLOW}6️⃣  (Opsiyonel) Arka planda çalıştır${NC}"
echo "   ./systemd_install.sh"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${BLUE}📚 Detaylı bilgi: KURULUM_REHBERI.md${NC}"
echo ""
