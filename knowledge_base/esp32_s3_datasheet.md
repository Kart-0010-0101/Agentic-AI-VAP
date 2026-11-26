# ESP32-S3-WROOM-1 Microcontroller & RF SoC Summary

- **Processor**: Dual-core Xtensa LX7 32-bit microprocessor, up to 240 MHz
- **Wireless Connectivity**: 2.4 GHz Wi-Fi (802.11 b/g/n) + Bluetooth 5.0 LE
- **SRAM / Flash**: 512 KB internal SRAM, up to 16 MB external QSPI Flash
- **ADC Channels**: Two 12-bit SAR ADCs (ADC1 & ADC2), up to 20 channels total; ADC2 shares RF frontend during active Wi-Fi transmission
- **Operating Voltage (VDD)**: 3.0 V to 3.6 V (nominal 3.3 V)
- **GPIO Max Current**: 40 mA max per pin (recommended <= 20 mA continuous)
- **Low-Power Deep Sleep**: ~7 uA typical with ULP RISC-V coprocessor polling sensors
- **Common Failure Pattern**: Reading ADC2 pins while Wi-Fi STA/AP is active returns ESP_ERR_TIMEOUT; always assign critical thermistor/voltage dividers to ADC1 GPIO1..GPIO10.
