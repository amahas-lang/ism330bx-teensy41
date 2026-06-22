#include <Wire.h>

#define IMU_ADDR  0x6B
#define WHO_AM_I  0x0F
#define CTRL1     0x10
#define CTRL2     0x11
#define CTRL3     0x12
#define STATUS    0x1E
#define OUTX_L_G  0x22
#define OUTX_L_A  0x28

void writeReg(uint8_t reg, uint8_t val) {
  Wire.beginTransmission(IMU_ADDR);
  Wire.write(reg);
  Wire.write(val);
  Wire.endTransmission();
}

uint8_t readReg(uint8_t reg) {
  Wire.beginTransmission(IMU_ADDR);
  Wire.write(reg);
  Wire.endTransmission(false);
  Wire.requestFrom((uint8_t)IMU_ADDR, (uint8_t)1);
  return Wire.read();
}

void readBytes(uint8_t reg, uint8_t* buf, uint8_t len) {
  Wire.beginTransmission(IMU_ADDR);
  Wire.write(reg);
  Wire.endTransmission(false);
  Wire.requestFrom((uint8_t)IMU_ADDR, (uint8_t)len);
  for (int i = 0; i < len; i++) buf[i] = Wire.read();
}

void setup() {
  Serial.begin(115200);
  Wire.begin();
  delay(20);

  if (readReg(WHO_AM_I) != 0x71) {
    Serial.println("ERROR: WHO_AM_I mismatch. Check wiring and CS pin.");
    while (1);
  }

  writeReg(CTRL3, 0x44);
  writeReg(CTRL1, 0x34);
  writeReg(CTRL2, 0x34);
  delay(50);
}

void loop() {
  if (readReg(STATUS) & 0x01) {
    uint8_t buf[6];

    readBytes(OUTX_L_A, buf, 6);
    int16_t ax = (int16_t)(buf[1] << 8 | buf[0]);
    int16_t ay = (int16_t)(buf[3] << 8 | buf[2]);
    int16_t az = (int16_t)(buf[5] << 8 | buf[4]);

    readBytes(OUTX_L_G, buf, 6);
    int16_t gx = (int16_t)(buf[1] << 8 | buf[0]);
    int16_t gy = (int16_t)(buf[3] << 8 | buf[2]);
    int16_t gz = (int16_t)(buf[5] << 8 | buf[4]);

    Serial.print(ax); Serial.print(",");
    Serial.print(ay); Serial.print(",");
    Serial.print(az); Serial.print(",");
    Serial.print(gx); Serial.print(",");
    Serial.print(gy); Serial.print(",");
    Serial.println(gz);
  }

  delay(20);
}
