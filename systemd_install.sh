#!/bin/bash

echo "=========================================="
echo "🔧 Systemd Servis Kurulumu"
echo "=========================================="
echo ""

# Renk kodları
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Kullanıcı adı ve çalışma dizini
CURRENT_USER=$(whoami)
CURRENT_DIR=$(pwd)

echo -e "${BLUE}👤 Kullanıcı: ${CURRENT_USER}${NC}"
echo -e "${BLUE}📁 Dizin: ${CURRENT_DIR}${NC}"
echo ""

# Onay iste
read -p "Systemd servisi olarak kurmak istiyor musunuz? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}❌ İptal edildi${NC}"
    exit 1
fi

# Servis dosyası oluştur
echo -e "${BLUE}📝 Servis dosyası oluşturuluyor...${NC}"

sudo tee /etc/systemd/system/polymarket-tracker.service > /dev/null << EOF
[Unit]
Description=Polymarket Telegram Tracker
After=network.target

[Service]
Type=simple
User=$CURRENT_USER
WorkingDirectory=$CURRENT_DIR
Environment="PATH=/usr/bin:/usr/local/bin"
ExecStart=/usr/bin/python3 telegram_tracker.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

echo -e "${GREEN}✅ Servis dosyası oluşturuldu${NC}"
echo ""

# Systemd'yi yeniden yükle
echo -e "${BLUE}🔄 Systemd yeniden yükleniyor...${NC}"
sudo systemctl daemon-reload

# Servisi etkinleştir
echo -e "${BLUE}✅ Servis etkinleştiriliyor...${NC}"
sudo systemctl enable polymarket-tracker

# Servisi başlat
echo -e "${BLUE}🚀 Servis başlatılıyor...${NC}"
sudo systemctl start polymarket-tracker

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Kurulum tamamlandı!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Durum kontrolü
sleep 2
echo -e "${BLUE}📊 Servis durumu:${NC}"
sudo systemctl status polymarket-tracker --no-pager -l

echo ""
echo -e "${YELLOW}📋 Kullanışlı komutlar:${NC}"
echo ""
echo "  • Durum kontrol:    sudo systemctl status polymarket-tracker"
echo "  • Logları görüntüle: sudo journalctl -u polymarket-tracker -f"
echo "  • Durdur:           sudo systemctl stop polymarket-tracker"
echo "  • Başlat:           sudo systemctl start polymarket-tracker"
echo "  • Yeniden başlat:   sudo systemctl restart polymarket-tracker"
echo ""
echo -e "${GREEN}🎉 Bot artık arka planda çalışıyor!${NC}"
echo -e "${BLUE}💬 Telegram'dan mesaj bekleyin...${NC}"
echo ""
