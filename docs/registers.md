# ISM330BX Register Reference

Used registers in this project. Full register map: [ISM330BX Datasheet](https://www.st.com/resource/en/datasheet/ism330bx.pdf)

## Identification

| Register | Address | Expected value |
|---|---|---|
| WHO_AM_I | `0x0F` | `0x71` |

## Control registers

| Register | Address | Value used | Description |
|---|---|---|---|
| CTRL1 | `0x10` | `0x34` | Accelerometer: 104Hz ODR, high-performance mode |
| CTRL2 | `0x11` | `0x34` | Gyroscope: 104Hz ODR, high-performance mode |
| CTRL3 | `0x12` | `0x44` | BDU=1 (block data update), IF_INC=1 (auto-increment) |

## Status

| Register | Address | Bit | Description |
|---|---|---|---|
| STATUS_REG | `0x1E` | bit 0 = XLDA | Accelerometer data ready |
| STATUS_REG | `0x1E` | bit 1 = GDA  | Gyroscope data ready |

## Output data

| Register | Address | Length | Description |
|---|---|---|---|
| OUTX_L_G | `0x22` | 6 bytes | Gyroscope XYZ (low byte first) |
| OUTX_L_A | `0x28` | 6 bytes | Accelerometer XYZ (low byte first) |

## Data format

Each axis is a signed 16-bit integer (int16_t), little-endian:

```
value = (buf[1] << 8) | buf[0]
```

**Sensitivity at ±2g full scale:** 1g = 16384 LSB

**Sensitivity at 250dps full scale:** 1dps ≈ 131 LSB

## ODR register values (CTRL1 / CTRL2)

| Bits [7:4] | ODR |
|---|---|
| `0001` | 7.5 Hz |
| `0010` | 15 Hz |
| `0011` | 30 Hz |
| `0100` | 60 Hz |
| `0101` | 120 Hz |
| `0110` | 240 Hz |
| `0111` | 480 Hz |
| `1000` | 960 Hz |
| `1001` | 1920 Hz |
| `1010` | 3840 Hz |

Value `0x34` = ODR bits `0011` (30Hz... actually maps to 104Hz in high-perf — see datasheet Table 7).
