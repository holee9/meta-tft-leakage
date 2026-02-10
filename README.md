# meta-tft-leakage

Yocto layer for aSi TFT 패널 누설 전류 감소 프로젝트입니다.

## 목표

i.MX8MP 플랫폼에서 TFT 패널 누설 전류 감소를 위한:
- SPI 드라이버 (Device Tree)
- TFT Leakage 제어 데몬
- Ethernet 통신 지원

## 구조

```
meta-tft-leakage/
├── conf/
│   └── layer.conf           # layer 정의
├── recipes-kernel/linux/
│   └── linux-imx8%.bbappend # Device Tree 추가
├── recipes-apps/
│   └── tft-leakage-daemon/  # 제어 데몬
└── recipes-core/images/
    └── tft-leakage-image.bb # 테스트 이미지 (선택)
```

## 사용 방법

### 1. Layer 추가

기존 Yocto 프로젝트의 `conf/bblayers.conf`에 추가:

```bash
bitbake-layers add-layer /path/to/meta-tft-leakage
```

또는 수동으로 추가:
```
/path/to/meta-tft-leakage \
```

### 2. 빌드

```bash
# 이미지에 데몬 추가
echo 'IMAGE_INSTALL:append = " tft-leakage-daemon"' >> conf/local.conf

# 빌드
bitbake your-image
```

## 레시피

### tft-leakage-daemon

TFT 패널 제어 데몬 패키지입니다.

**기능:**
- FPGA SPI 통신
- Bias 전압 제어
- Dummy Scan 제어
- Ethernet 서버 (선택)

### Device Tree

i.MX8MP에 SPI 인터페이스를 추가합니다:

```
ecspi1: spi@30830000 {
    compatible = "fsl,imx8mp-ecspi";
    ...
    cs-gpios = <&gpio5 9 GPIO_ACTIVE_LOW>;
    ...
    tft-panel@0 {
        compatible = "tft,panel-controller";
        reg = <0>;
        spi-max-frequency = <25000000>;
        ...
    };
};
```

## 의존성

- `meta-bsp` (i.MX8MP BSP)
- `openembedded-core` (OE-Core)

## 호환성

| 플랫폼 | BSP 버전 | Yocto |
|--------|----------|-------|
| i.MX8MP | rel_imx_5.15.._2.0.0 | kirkstone |

## 라이선스

MIT License - [LICENSE](LICENSE)

## 문서

### 배포 패키지

| 문서 | 설명 |
|------|------|
| [README.md](docs/delivery/README.md) | 배포 패키지 개요 |
| [00_project_overview.md](docs/delivery/00_project_overview.md) | 프로젝트 개요 및 시스템 역할 |
| [01_platform_specifications.md](docs/delivery/01_platform_specifications.md) | i.MX8MP 플랫폼 사양 |
| [02_spi_driver_requirements.md](docs/delivery/02_spi_driver_requirements.md) | SPI 드라이버 요구사항 |
| [03_device_tree_configuration.md](docs/delivery/03_device_tree_configuration.md) | Device Tree 설정 |
| [04_kernel_config.md](docs/delivery/04_kernel_config.md) | 커널 설정 |
| [05_userspace_interface.md](docs/delivery/05_userspace_interface.md) | 유저스페이스 인터페이스 |
| [06_temperature_monitoring.md](docs/delivery/06_temperature_monitoring.md) | 온도 모니터링 |
| [07_ethernet_communication.md](docs/delivery/07_ethernet_communication.md) | Ethernet 통신 |
| [08_acceptance_criteria.md](docs/delivery/08_acceptance_criteria.md) | 인수 기준 |
| [reference/](docs/delivery/reference/) | 참고 문서 (Arrhenius 모델 등) |

### 요약 사양

- [docs/spec.md](docs/spec.md) - 간단 사양 요약

## 관련 프로젝트

- [tft-panel-fpga](https://github.com/holee9/tft-panel-fpga) - FPGA RTL
- [TftLeakage.Hardware](https://github.com/holee9/TftLeakage.Hardware) - .NET 라이브러리
