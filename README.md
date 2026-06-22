# ISM330BX — Teensy 4.1

Read accelerometer and gyroscope data from the ISM330BX IMU over I²C on a Teensy 4.1, with a live 3D visualizer in Python.

---

## Hardware

### Sensor

The **ISM330BX** is a 6-axis IMU from STMicroelectronics. This guide uses it on the **STEVAL-MKI245KA** breakout board, which has the chip soldered to the center with decoupling capacitors included.

| | |
|---|---|
| Accelerometer | ±2 / ±4 / ±8 g |
| Gyroscope | ±125 to ±4000 dps |
| Interface | I²C / SPI / MIPI I3C |
| I²C address (CS → 3.3V) | `0x6B` |
| WHO_AM_I | `0x0F` → `0x71` |

- [ISM330BX Datasheet](https://www.st.com/resource/en/datasheet/ism330bx.pdf)
- [STEVAL-MKI245KA Product page](https://www.st.com/en/evaluation-tools/steval-mki245ka.html)

### Wiring

```
Teensy 4.1            STEVAL-MKI245KA
----------            ---------------
3.3V          ──────► VDD
GND           ──────► GND
SDA (pin 18)  ──────► SDA
SCL (pin 19)  ──────► SCL
3.3V          ──────► CS    ← required for I²C mode
```

> ⚠️ **CS must be tied to 3.3V.** Without this the sensor stays in SPI mode and will not respond on I²C.

---

## Requirements

- [VS Code](https://code.visualstudio.com/) + [PlatformIO](https://platformio.org/)
- Python 3
- Ubuntu / Linux

```bash
pip install pygame pyserial --break-system-packages
```

---

## Usage

### 1. Flash the Teensy

```bash
cd teensy_firmware
pio run --target upload
```

### 2. Run the visualizer

```bash
# Find the port
ls /dev/ttyACM*

# Run
python3 visualizer/imu_visualizer.py
```

If the port is not `/dev/ttyACM0`, update the `PORT` variable at the top of `imu_visualizer.py`.

> After a reboot, re-flash the Teensy before running the visualizer.

---

## Output

The firmware streams CSV over USB Serial at 115200 baud:

```
AX,AY,AZ,GX,GY,GZ
```

At ±2g full scale: **1g ≈ 16384 LSB**

---

## Troubleshooting

| Problem | Fix |
|---|---|
| No I²C device found | Check CS → 3.3V |
| WHO_AM_I returns wrong value | Check CS wiring and I²C address `0x6B` |
| All data is 0 | Read back CTRL1/CTRL2, should be `0x34` |
| Cannot open `/dev/ttyACM*` | Run `ls /dev/ttyACM*` and update PORT |
| Visualizer frozen | Re-flash Teensy and press reset |
