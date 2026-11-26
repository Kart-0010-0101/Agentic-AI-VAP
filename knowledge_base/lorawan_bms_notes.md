# SX1276 LoRaWAN Sub-GHz Transceiver & LiFePO4 BMS Field Notes

## SX1276 RF Module
- **Frequency Bands**: 865 - 867 MHz (IN865 India), 868 MHz (EU868), 915 MHz (US915)
- **Link Budget**: Up to 168 dB (Sensitivity -148 dBm at SF12, BW 125 kHz)
- **Spreading Factors**: SF7 (highest rate, ~5.5 kbps) to SF12 (longest range, ~290 bps)
- **Max TX Power**: +20 dBm (+14 dBm typical regulatory cap)

## 4S LiFePO4 Battery Management System (BMS)
- **Nominal Voltage**: 12.8 V (3.2 V per cell)
- **Full Charge Cutoff**: 14.6 V (3.65 V/cell)
- **Over-Discharge Cutoff**: 10.0 V (2.50 V/cell)
- **Temperature Interlock**: Disable charging below 0 C to prevent metallic lithium plating.
