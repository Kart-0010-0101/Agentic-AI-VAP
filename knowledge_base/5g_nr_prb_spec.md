# 5G NR gNodeB FR1 Physical Resource Block (PRB) & Fault Spec

- **Frequency Range 1 (FR1)**: 410 MHz to 7125 MHz (Band n78: 3300 - 3800 MHz)
- **Subcarrier Spacing (SCS)**: 30 kHz (typical for TDD n78 macro/micro cells)
- **100 MHz Channel Bandwidth**: 273 PRBs max (12 subcarriers per PRB = 3276 active subcarriers)
- **Critical SLA Thresholds**:
  - PRB Utilization > 85% for 3 consecutive windows -> trigger Congestion Load Balance alert
  - SINR < 3.0 dB or RSRP < -112 dBm -> Edge coverage degradation / handover failure risk
  - BLER (Block Error Rate) > 10% -> Trigger MCS (Modulation Coding Scheme) step-down
- **Common Root Causes**: Sector tilt mismatch, external L-band/C-band uplink interference, backhaul SCTP jitter.
