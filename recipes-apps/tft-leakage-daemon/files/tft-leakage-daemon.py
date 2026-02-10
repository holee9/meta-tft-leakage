#!/usr/bin/env python3
"""
TFT Panel Leakage Control Daemon

Purpose: Control TFT panel FPGA for leakage reduction
Target: i.MX8MP Linux
"""

import sys
import time
import signal
import logging
import json
from spidev import SpiDev

# Configuration
CONFIG_PATH = "/etc/tft-leakage/appsettings.json"
SPI_BUS = 0
SPI_DEVICE = 0
SPI_MAX_SPEED = 25000000  # 25 MHz

# Register addresses
REG_CTRL = 0x00
REG_STATUS = 0x01
REG_BIAS_SEL = 0x02
REG_SCAN_CONFIG = 0x04
REG_VERSION = 0xFE

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('tft-leakage-daemon')


class TftPanelController:
    """TFT Panel FPGA Controller via SPI"""

    def __init__(self, bus=SPI_BUS, device=SPI_DEVICE):
        self.spi = SpiDev()
        self.bus = bus
        self.device = device
        self.connected = False

    def connect(self):
        """Connect to FPGA via SPI"""
        try:
            self.spi.open(self.bus, self.device)
            self.spi.max_speed_hz = SPI_MAX_SPEED
            self.spi.mode = 0  # CPOL=0, CPHA=0
            self.connected = True
            logger.info(f"Connected to SPI bus {self.bus}, device {self.device}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to SPI: {e}")
            return False

    def disconnect(self):
        """Disconnect SPI"""
        if self.connected:
            self.spi.close()
            self.connected = False
            logger.info("Disconnected from SPI")

    def read_register(self, addr):
        """Read from FPGA register"""
        if not self.connected:
            return None

        try:
            # Write address (read command could be defined differently)
            # For now, using simple write-then-read pattern
            self.spi.writebytes([addr, 0x00, 0x00, 0x00, 0x00])
            time.sleep(0.001)
            data = self.spi.readbytes(4)
            value = (data[0] << 24) | (data[1] << 16) | (data[2] << 8) | data[3]
            return value
        except Exception as e:
            logger.error(f"Failed to read register {addr:02X}: {e}")
            return None

    def write_register(self, addr, value):
        """Write to FPGA register"""
        if not self.connected:
            return False

        try:
            # SPI write: address (8-bit) + data (32-bit)
            bytes_to_write = [
                addr,
                (value >> 24) & 0xFF,
                (value >> 16) & 0xFF,
                (value >> 8) & 0xFF,
                value & 0xFF
            ]
            self.spi.writebytes(bytes_to_write)
            logger.debug(f"Wrote register {addr:02X} = 0x{value:08X}")
            return True
        except Exception as e:
            logger.error(f"Failed to write register {addr:02X}: {e}")
            return False

    def get_version(self):
        """Get FPGA firmware version"""
        version = self.read_register(REG_VERSION)
        if version:
            # Convert to string (e.g., 0x56313030 -> "V10")
            version_str = ''.join([chr((version >> (8 * (3 - i))) & 0xFF)
                                  for i in range(4) if (version >> (8 * (3 - i))) & 0xFF])
            return version_str
        return None

    def set_idle_mode(self, enable):
        """Enable or disable idle mode"""
        value = 1 if enable else 0
        return self.write_register(REG_CTRL, value)

    def set_bias(self, bias_sel):
        """Set bias voltage selection (0-7)"""
        if 0 <= bias_sel <= 7:
            return self.write_register(REG_BIAS_SEL, bias_sel)
        return False


class TftLeakageDaemon:
    """Main daemon class"""

    def __init__(self):
        self.controller = TftPanelController()
        self.running = False
        self.config = {}

    def load_config(self):
        """Load configuration from file"""
        try:
            with open(CONFIG_PATH, 'r') as f:
                self.config = json.load(f)
            logger.info(f"Loaded configuration from {CONFIG_PATH}")
        except Exception as e:
            logger.warning(f"Failed to load config: {e}, using defaults")
            self.config = {
                "idle_enabled": True,
                "bias_voltage": 2,
                "scan_interval_ms": 1000
            }

    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, shutting down...")
        self.running = False

    def initialize(self):
        """Initialize the daemon"""
        logger.info("Initializing TFT Leakage Daemon...")

        self.load_config()

        if not self.controller.connect():
            logger.error("Failed to connect to FPGA controller")
            return False

        # Check FPGA version
        version = self.controller.get_version()
        if version:
            logger.info(f"FPGA firmware version: {version}")
        else:
            logger.warning("Could not read FPGA version")

        return True

    def run(self):
        """Main daemon loop"""
        self.running = True

        logger.info("Daemon started")

        while self.running:
            try:
                # Main control loop
                # TODO: Implement idle state detection and control
                time.sleep(1)

            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(1)

        logger.info("Daemon stopped")

    def shutdown(self):
        """Cleanup and shutdown"""
        logger.info("Shutting down...")
        self.controller.disconnect()


def main():
    """Main entry point"""
    daemon = TftLeakageDaemon()

    daemon.setup_signal_handlers()

    if not daemon.initialize():
        logger.error("Initialization failed")
        sys.exit(1)

    try:
        daemon.run()
    except KeyboardInterrupt:
        pass
    finally:
        daemon.shutdown()


if __name__ == "__main__":
    main()
