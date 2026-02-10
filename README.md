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

## 관련 프로젝트

- [tft-panel-fpga](https://github.com/holee9/tft-panel-fpga) - FPGA RTL
- [TftLeakage.Hardware](https://github.com/holee9/TftLeakage.Hardware) - .NET 라이브러리
