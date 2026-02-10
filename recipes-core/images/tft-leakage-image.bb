# TFT Leakage Test Image
# This recipe creates a test image with TFT leakage support

IMAGE_INSTALL = "packagegroup-core-boot \
                 packagegroup-core-ssh-openssh \
                 python3 python3-spidev \
                 tft-leakage-daemon \
                 kernel-modules \
                 ${CORE_IMAGE_EXTRA_INSTALL}"

IMAGE_LINGUAS = " "

LICENSE = "MIT"

IMAGE_ROOTFS_SIZE ?= "8192"
IMAGE_ROOTFS_EXTRA_SPACE:append = "${@bb.utils.contains("DISTRO_FEATURES", "systemd", " + 4096", "", d)}"

inherit core-image

# Enable systemd
IMAGE_FEATURES += "ssh-server-openssh"

# Add TFT leakage specific configurations
ROOTFS_POSTPROCESS_COMMAND += "configure_tft_leakage; "

configure_tft_leakage() {
    # Install TFT leakage service
    if [ -d ${IMAGE_ROOTFS}${systemd_system_unitdir} ]; then
        ln -sf ${systemd_system_unitdir}/tft-leakage-daemon.service \
              ${IMAGE_ROOTFS}${sysconfdir}/systemd/system/multi-user.target.wants/
    fi
}
