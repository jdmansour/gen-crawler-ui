FROM mcr.microsoft.com/playwright:v1.49.0-noble

# Install any additional dependencies you need
RUN apt-get update && apt-get install -y \
    curl \
    fonts-liberation \
    fonts-noto \
    unzip \
    socat \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Create directory for extensions
RUN mkdir -p /opt/extensions

# Download and add uBlock Origin Lite (Manifest V3)
# Get the latest version from: https://github.com/uBlockOrigin/uBOL-home/releases
ADD https://github.com/uBlockOrigin/uBOL-home/releases/download/2026.215.1801/uBOLite_2026.215.1801.chromium.zip /tmp/ubol.zip
RUN unzip /tmp/ubol.zip -d /opt/extensions/ubol && rm /tmp/ubol.zip

# Download and add "I still don't care about cookies" (cookie consent auto-dismiss)
# Get the latest version from: https://github.com/OhMyGuus/I-Still-Dont-Care-About-Cookies/releases
ADD https://github.com/OhMyGuus/I-Still-Dont-Care-About-Cookies/releases/download/v1.1.9/ISDCAC-chrome-source.zip /tmp/isdcac.zip
RUN unzip /tmp/isdcac.zip -d /opt/extensions/isdcac && rm /tmp/isdcac.zip

# Resolve Chromium binary path installed by Playwright (version-independent)
RUN CHROME_BIN=$(find /ms-playwright -name chrome -type f -path '*/chrome-linux/*' | head -1) \
    && ln -s "$CHROME_BIN" /usr/local/bin/chrome

# Set extension paths as environment variables for easy reference
ENV UBOL_EXT_PATH=/opt/extensions/ubol
ENV ISDCAC_EXT_PATH=/opt/extensions/isdcac

# Expose port for CDP remote debugging
EXPOSE 9222

# Entrypoint script starts Xvfb, Chrome (CDP on 127.0.0.1:9223), and socat
# (forwarding 0.0.0.0:9222 -> 127.0.0.1:9223).
# Xvfb is needed so --force-device-scale-factor=2 works (ignored in headless mode).
# --remote-debugging-address=0.0.0.0 is broken, so socat exposes CDP externally.
COPY browser-entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
CMD ["/entrypoint.sh"]
