SUMMARY = "TFT Panel Leakage Control Daemon"
DESCRIPTION = "Daemon for controlling TFT panel leakage reduction via FPGA SPI interface"
SECTION = "applications"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=xxxx"

SRC_URI = "file://tft-leakage-daemon.py \
           file://tft-leakage-daemon.service \
           file://appsettings.json \
           file://LICENSE"

RDEPENDS:${PN} = "python3-core python3-spidev python3-logging"

S = "${WORKDIR}"

do_install() {
    install -d ${D}${bindir}
    install -m 0755 ${S}/tft-leakage-daemon.py ${D}${bindir}/tft-leakage-daemon

    install -d ${D}${sysconfdir}/tft-leakage
    install -m 0644 ${S}/appsettings.json ${D}${sysconfdir}/tft-leakage/appsettings.json

    install -d ${D}${systemd_system_unitdir}
    install -m 0644 ${S}/tft-leakage-daemon.service ${D}${systemd_system_unitdir}

    install -d ${D}${docdir}/${PN}
    install -m 0644 ${S}/LICENSE ${D}${docdir}/${PN}/
}

FILES:${PN} += "${bindir}/tft-leakage-daemon \
                ${sysconfdir}/tft-leakage/appsettings.json"

SYSTEMD_SERVICE:${PN} = "tft-leakage-daemon.service"
SYSTEMD_AUTO_ENABLE = "enable"
