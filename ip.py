# -*- coding: utf-8 -*-
# Developer: HIDDEN KING

import http.server
import socketserver
import json

PORT = int(input("🔢 Enter port number (e.g., 8080): "))

HTML_PAGE = r"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>HIDDEN KING</title>
<style>
body {
    background: #0d0d0d;
    color: #fff;
    font-family: Arial, sans-serif;
    text-align: center;
    margin: 0;
    padding: 0;
}
header {
    font-size: 1.4rem;
    font-weight: bold;
    padding: 20px;
    color: #ff3333;
}
button {
    background: none;
    border: 2px solid #ff3333;
    padding: 12px 25px;
    color: #fff;
    font-size: 1.1rem;
    cursor: pointer;
    border-radius: 8px;
    transition: 0.3s ease;
}
button:hover {
    background: #ff3333;
    color: #000;
    transform: scale(1.05);
}
pre {
    text-align: left;
    margin: 20px auto;
    max-width: 90%;
    background: #1a1a1a;
    padding: 15px;
    border-radius: 10px;
    overflow-x: auto;
    font-size: 0.95rem;
}
</style>
</head>
<body>
<header>HIDDEN KING</header>
<button onclick="collectInfo()">Click Me</button>
<pre id="output"></pre>
<script>
async function collectInfo() {
    const now = new Date();

    // Public IP and Location Info
    let ipData = {};
    try {
        let res = await fetch('https://ipapi.co/json/');
        ipData = await res.json();
    } catch (e) {}

    // GPU Info
    const gl = document.createElement('canvas').getContext('webgl');
    let gpu = "N/A";
    if (gl) {
        const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
        if (debugInfo) gpu = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);
    }

    // Canvas Fingerprint
    let canvas2d = document.createElement('canvas');
    let ctx = canvas2d.getContext('2d');
    ctx.textBaseline = "top";
    ctx.font = "14px 'Arial'";
    ctx.fillText("HIDDENKING", 2, 2);
    let canvasHash = canvas2d.toDataURL();

    let info = {
        "🆔 Public IP": ipData.ip || "N/A",
        "🏙️ City": ipData.city || "N/A",
        "🌍 Region": ipData.region || "N/A",
        "🇮🇳 Country": ipData.country_name || "N/A",
        "📡 ISP": ipData.org || "N/A",
        "⏰ Time": now.toString(),
        "📅 Local Date": now.toLocaleString(),
        "🌐 Timezone": Intl.DateTimeFormat().resolvedOptions().timeZone,
        "🔧 Product Sub": navigator.productSub,
        "🏷️ Vendor": navigator.vendor,
        "👆 Max Touch Points": navigator.maxTouchPoints,
        "🚫 Do Not Track": navigator.doNotTrack,
        "⚙️ Hardware Cores": navigator.hardwareConcurrency,
        "🍪 Cookies Enabled": navigator.cookieEnabled,
        "🔤 App Code Name": navigator.appCodeName,
        "🖥️ App Name": navigator.appName,
        "📲 App Version": navigator.appVersion,
        "💻 Platform": navigator.platform,
        "🛠️ Product": navigator.product,
        "👤 User Agent": navigator.userAgent,
        "🗣️ Language": navigator.language,
        "🌍 Languages": navigator.languages.join(", "),
        "🤖 Webdriver": navigator.webdriver ? "Yes" : "No",
        "📄 PDF Viewer Enabled": navigator.mimeTypes['application/pdf'] ? "Yes" : "No",
        "🧠 Device Memory": (navigator.deviceMemory || "N/A") + " GB",
        "🖼️ Screen Size": screen.width + "x" + screen.height,
        "📏 Viewport Size": window.innerWidth + "x" + window.innerHeight,
        "🎨 GPU": gpu,
        "🖌️ Canvas Fingerprint": canvasHash,
        "📦 Plugins": Array.from(navigator.plugins).map(p => p.name).join(", "),
        "🎵 Audio Sample Rate": (new (window.AudioContext||window.webkitAudioContext)()).sampleRate + " Hz",
        "↩️ Referrer": document.referrer || "None",
        "👁️ Tab Visibility": document.visibilityState,
        "🖱️ Mouse Buttons": navigator.maxTouchPoints > 0 ? "Touch Device" : "Mouse Detected",
        "⌨️ Keyboard Layout": navigator.language,
    };

    try {
        const battery = await navigator.getBattery();
        info["🔋 Battery Level"] = Math.round(battery.level * 100) + "%";
        info["⚡ Charging"] = battery.charging ? "Yes" : "No";
    } catch {}

    try {
        if (navigator.connection) {
            info["📶 Network Type"] = navigator.connection.type || "N/A";
            info["📡 Effective Type"] = navigator.connection.effectiveType || "N/A";
            info["⏱️ RTT"] = navigator.connection.rtt + " ms";
            info["⬇️ Downlink"] = navigator.connection.downlink + " Mbps";
            info["💾 Save Data"] = navigator.connection.saveData ? "Yes" : "No";
        }
    } catch {}

    try {
        const devices = await navigator.mediaDevices.enumerateDevices();
        info["🎤 Audio Input"] = devices.some(d => d.kind === 'audioinput') ? "Available" : "Not available";
        info["🎥 Video Input"] = devices.some(d => d.kind === 'videoinput') ? "Available" : "Not available";
        info["🔈 Audio Output"] = devices.some(d => d.kind === 'audiooutput') ? "Available" : "Not available";
        info["📷 Camera Count"] = devices.filter(d => d.kind === 'videoinput').length;
    } catch {}

    try {
        if (navigator.storage && navigator.storage.estimate) {
            const {usage, quota} = await navigator.storage.estimate();
            info["💽 Storage Used"] = (usage / (1024*1024)).toFixed(2) + " MB";
            info["💽 Storage Quota"] = (quota / (1024*1024)).toFixed(2) + " MB";
        }
    } catch {}

    // Approx Uptime
    info["⏳ Uptime (sec)"] = Math.round(performance.now() / 1000);

    document.getElementById("output").textContent = Object.entries(info)
        .map(([k,v]) => `${k}: ${v}`).join("\\n");

    // Send info to Python backend for Termux display
    fetch('/log', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(info)
    });
}
</script>
</body>
</html>
"""

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode())
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        if self.path == "/log":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                info = json.loads(post_data.decode())
                print("\n📋 Device Info Collected:")
                for k, v in info.items():
                    print(f"{k}: {v}")
                print("\n" + "="*50)
            except:
                print("Error parsing received data")
            self.send_response(200)
            self.end_headers()

with socketserver.TCPServer(("localhost", PORT), Handler) as httpd:
    print(f"🌍 Open in browser: http://localhost:{PORT}")
    httpd.serve_forever()