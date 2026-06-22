import pygame
import serial
import math
import sys

PORT = '/dev/ttyACM0'
BAUD = 115200


def draw_box(screen, roll, pitch, cx, cy):
    w, h, d = 120, 30, 50
    points = [
        [-w, -h, -d], [ w, -h, -d], [ w,  h, -d], [-w,  h, -d],
        [-w, -h,  d], [ w, -h,  d], [ w,  h,  d], [-w,  h,  d],
    ]

    r = math.radians(roll)
    p = math.radians(pitch)

    def rot(x, y, z):
        x1 = x * math.cos(r) - y * math.sin(r)
        y1 = x * math.sin(r) + y * math.cos(r)
        y2 = y1 * math.cos(p) - z * math.sin(p)
        z2 = y1 * math.sin(p) + z * math.cos(p)
        return x1, y2, z2

    proj = []
    for px, py, pz in points:
        x, y, z = rot(px, py, pz)
        s = 400 / (400 + z)
        proj.append((int(cx + x * s), int(cy - y * s), z))

    faces = [
        ([0, 1, 2, 3], (30,  100, 200)),
        ([4, 5, 6, 7], (30,  100, 200)),
        ([0, 1, 5, 4], (20,  160,  80)),
        ([2, 3, 7, 6], (20,  160,  80)),
        ([0, 3, 7, 4], (60,   60, 180)),
        ([1, 2, 6, 5], (60,   60, 180)),
    ]

    for face, color in sorted(faces, key=lambda f: sum(proj[i][2] for i in f[0])):
        pts = [(proj[i][0], proj[i][1]) for i in face]
        pygame.draw.polygon(screen, color, pts)
        pygame.draw.polygon(screen, (200, 200, 200), pts, 2)


def main():
    try:
        ser = serial.Serial(PORT, BAUD, timeout=0.1)
    except Exception:
        print(f"Cannot open {PORT} — check port with: ls /dev/ttyACM*")
        sys.exit(1)

    pygame.init()
    W, H = 800, 600
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("ISM330BX Visualizer — Esc to quit")
    font = pygame.font.SysFont("monospace", 28, bold=True)
    clock = pygame.time.Clock()

    roll = pitch = 0.0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit(); return

        try:
            parts = ser.readline().decode('utf-8').strip().split(',')
            if len(parts) == 6:
                ax, ay, az = int(parts[0]), int(parts[1]), int(parts[2])
                s = 16384.0
                ax_g, ay_g, az_g = ax / s, ay / s, az / s
                new_roll  = math.degrees(math.atan2(ay_g, az_g))
                new_pitch = math.degrees(math.atan2(-ax_g, math.sqrt(ay_g**2 + az_g**2)))
                roll  = 0.85 * roll  + 0.15 * new_roll
                pitch = 0.85 * pitch + 0.15 * new_pitch
        except Exception:
            pass

        screen.fill((20, 20, 30))
        draw_box(screen, roll, pitch, W // 2, H // 2)
        screen.blit(font.render(f"Roll:  {roll:+.1f}\u00b0", True, (255, 220, 0)), (20, 20))
        screen.blit(font.render(f"Pitch: {pitch:+.1f}\u00b0", True, (255, 220, 0)), (20, 60))
        pygame.display.flip()
        clock.tick(50)


if __name__ == "__main__":
    main()
