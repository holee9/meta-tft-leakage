# Yocto Layer Specification for TFT Leakage Reduction

## Summary

이 문서는 aSi TFT 패널 누설 전류 감소 프로젝트를 위한 Yocto Layer 사양서입니다.

## 목차

1. [프로젝트 개요](#1-프로젝트-개요)
2. [플랫폼 사양](#2-플랫폼-사양)
3. [SPI 드라이버 요구사항](#3-spi-드라이버-요구사항)
4. [Device Tree 설정](#4-device-tree-설정)
5. [커널 설정](#5-커널-설정)
6. [유저스페이스 인터페이스](#6-유저스페이스-인터페이스)
7. [Ethernet 통신](#7-ethernet-통신)
8. [인수 기준](#8-인수-기준)

---

## 1. 프로젝트 개요

### 목표

- i.MX8MP 플랫폼에 SPI 드라이버 추가 (비침투적)
- FPGA 제어 데몬 구현
- Ethernet 통신 지원
- 기존 Yocto 빌드 훼손하지 않는 모듈형 구조

### 배포 방식

**Yocto Layer (meta-tft-leakage)**
- `bbappend`만 사용하여 기존 레시피 수정 없음
- Device Tree는 overlay 형태로 추가
- 새 데몬은 독립 패키지

---

## 2. 플랫폼 사양

### 하드웨어

| 항목 | 사양 |
|------|------|
| SoC | NXP i.MX8MP |
| BSP | rel_imx_5.15.._2.0.0 |
| Yocto | kirkstone (4.0) |
| SPI | ECSPI1 (max 25MHz) |
| Ethernet | 1Gbps (eth0/eth1) |

### 소프트웨어

| 항목 | 버전 |
|------|------|
| Kernel | 5.15.x |
| systemd | latest |
| Python | 3.10+ |

---

## 3. SPI 드라이버 요구사항

### 기능 요구사항

- [REQ-YOCTO-001] Linux SPI spidev 드라이버 활성화
- [REQ-YOCTO-002] ECSPI1을 TFT 제어용으로 할당
- [REQ-YOCTO-003] SPI 모드 0 (CPOL=0, CPHA=0) 지원
- [REQ-YOCTO-004] 최대 25MHz 클럭 지원

### Device Tree

```
ecspi1: spi@30830000 {
    compatible = "fsl,imx8mp-ecspi";
    cs-gpios = <&gpio5 9 GPIO_ACTIVE_LOW>;
    spi-max-frequency = <25000000>;
    ...
}
```

---

## 4. Device Tree 설정

### 장치 경로

- **ECSPI1**: 0x30830000
- **CS GPIO**: GPIO5_IO9
- **핀 mux**: SCLK, MOSI, MISO, SS0

### 핀 설정

| 신호 | Pad | Alt Function |
|------|-----|--------------|
| SCLK | ECSPI1_SCLK | ALT5 |
| MOSI | ECSPI1_MOSI | ALT5 |
| MISO | ECSPI1_MISO | ALT5 |
| SS0 | ECSPI1_SS0 | GPIO (CS control) |

---

## 5. 커널 설정

### 필수 커널 옵션

```
CONFIG_SPI=y
CONFIG_SPI_MASTER=y
CONFIG_SPI_IMX=y
CONFIG_SPI_SPIDEV=y
CONFIG_GPIO_SYSFS=y
```

---

## 6. 유저스페이스 인터페이스

### SPI 장치 노드

```
/dev/spidev0.0  - ECSPI1 CS0 (TFT Panel)
```

### 데몬 서비스

```
tft-leakage-daemon.service
- ExecStart: /usr/bin/tft-leakage-daemon
- Restart: always
- After: network.target
```

---

## 7. Ethernet 통신

### 포트

| 포트 | 용도 |
|------|------|
| 8080 | TCP 상태 요청/응답 |
| 8081 | UDP 이벤트 알림 |

### 프로토콜

- **TCP**: 상태 조회, 제어 명령
- **UDP**: 비동기 이벤트 알림

---

## 8. 인수 기준

### 기능 테스트

- [TEST-YOCTO-001] spidev 장치 노드 생성 확인
- [TEST-YOCTO-002] SPI 쓰기/읽기 동작 확인
- [TEST-YOCTO-003] 데몬 서비스 시작 확인
- [TEST-YOCTO-004] Ethernet 포트 Listening 확인

### 비침투성 검증

- [TEST-YOCTO-101] 기존 레시피 수정 없음 확인
- [TEST-YOCTO-102] bbappend만 사용 확인
- [TEST-YOCTO-103] layer 제거 시 동작 복귀 확인

---

## 참고 문서

- [docs/delivery/to-yocto-project/](https://github.com/holee9/TFT-Leak-plan/tree/main/docs/delivery/to-yocto-project) - 상세 사양서
