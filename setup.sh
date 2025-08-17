#!/bin/bash
# setup.sh - Installer for ip.py tool
# Developer: HiDDEN KING

# Colors
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
CYAN='\033[1;36m'
RESET='\033[0m'

clear
echo -e "${CYAN}"
echo "╔════════════════════════════════════════╗"
echo "║      ⚡ HiDDEN KING - IP Tool Setup ⚡   ║"
echo "╚════════════════════════════════════════╝"
echo -e "${RESET}"

# Update packages
echo -e "${YELLOW}[+] Updating system packages...${RESET}"
pkg update -y && pkg upgrade -y

# Install python
echo -e "${YELLOW}[+] Installing Python...${RESET}"
pkg install -y python

# Install pip (if not present)
echo -e "${YELLOW}[+] Installing pip...${RESET}"
pkg install -y python-pip

# Install required Python packages
echo -e "${YELLOW}[+] Installing required Python modules...${RESET}"
pip install --upgrade pip
pip install requests flask colorama

# Make ip.py executable
if [ -f "ip.py" ]; then
    chmod +x ip.py
    echo -e "${GREEN}[✓] ip.py found and made executable${RESET}"
else
    echo -e "${RED}[!] ip.py not found in this directory!${RESET}"
fi

# Finish banner
echo -e "${CYAN}"
echo "╔════════════════════════════════════════╗"
echo "║   🎉 Installation Completed! 🎉         ║"
echo "╠════════════════════════════════════════╣"
echo "║  Run the tool using:                   ║"
echo "║  ${GREEN}python ip.py${RESET}                        ║"
echo "║                                        ║"
echo "║  Developed by: ${RED}HiDDEN KING${RESET}             ║"
echo "╚════════════════════════════════════════╝"
echo -e "${RESET}"