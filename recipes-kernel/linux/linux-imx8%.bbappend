# TFT Leakage Device Tree Overlay
# This bbappend adds TFT panel controller device tree overlay

FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

SRC_URI += "file://imx8mp-tft-leakage.dts"

# The overlay will be built and installed as part of kernel build
# No additional compilation steps needed
