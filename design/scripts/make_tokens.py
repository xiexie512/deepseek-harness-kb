#!/usr/bin/env python3
"""按种子色生成一套完整的设计 token（CSS）。

用法：
    python3 make_tokens.py --seed "#2563eb"
    python3 make_tokens.py --seed "#0f766e" --mode dark
    python3 make_tokens.py --seed "#7c3aed" --mode both --out tokens.css

输出包含：品牌色阶、中性色阶、语义色、亮/暗双主题、间距/字阶/行高/圆角/阴影/动效。
"""

import argparse
import colorsys
import re
import sys

# ---------------------------------------------------------------- color utils


def hex_to_rgb(h):
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if not re.fullmatch(r"[0-9a-fA-F]{6}", h):
        raise ValueError(f"无法识别的颜色: {h}")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#" + "".join(f"{max(0, min(255, round(v))):02x}" for v in rgb)


def hex_to_hsl(h):
    r, g, b = (v / 255 for v in hex_to_rgb(h))
    hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
    return hh * 360, ss, ll


def hsl_to_hex(hh, ss, ll):
    hh = (hh % 360) / 360
    ss = max(0.0, min(1.0, ss))
    ll = max(0.0, min(1.0, ll))
    r, g, b = colorsys.hls_to_rgb(hh, ll, ss)
    return rgb_to_hex((r * 255, g * 255, b * 255))


def rel_lum(hex_color):
    def chan(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = hex_to_rgb(hex_color)
    return 0.2126 * chan(r) + 0.7152 * chan(g) + 0.0722 * chan(b)


def contrast(a, b):
    la, lb = rel_lum(a), rel_lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


# ---------------------------------------------------------------- ramps

LEVELS = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900]

# 每档的目标亮度与饱和度系数（以 500 为种子色本身）
LIGHT_L = {50: 0.972, 100: 0.940, 200: 0.880, 300: 0.790, 400: 0.680}
LIGHT_S = {50: 0.45, 100: 0.60, 200: 0.75, 300: 0.87, 400: 0.95}
# 深色档按种子色亮度等比下压，保证任何种子色都能得到单调递减的色阶
DARK_F = {600: 0.80, 700: 0.65, 800: 0.50, 900: 0.36}


def make_ramp(seed, hue_shift=0.0):
    h, s, l0 = hex_to_hsl(seed)
    h = (h + hue_shift) % 360
    ramp = {}
    for lv in LEVELS:
        if lv == 500:
            ramp[lv] = hsl_to_hex(h, s, l0)
        elif lv < 500:
            ramp[lv] = hsl_to_hex(h, s * LIGHT_S[lv], LIGHT_L[lv])
        else:
            ramp[lv] = hsl_to_hex(h, min(1.0, s * (DARK_F[lv] + 0.18)),
                                 max(0.10, l0 * DARK_F[lv]))
    return ramp


def build_neutral(seed):
    """中性色：继承种子色相，饱和度极低，保证'有倾向的灰'。"""
    h, _, _ = hex_to_hsl(seed)
    sat = 0.09
    levels = {50: 0.982, 100: 0.962, 200: 0.912, 300: 0.83,
              400: 0.70, 500: 0.55, 600: 0.42, 700: 0.30,
              800: 0.20, 900: 0.11}
    return {lv: hsl_to_hex(h, sat if lv < 800 else sat * 0.8, levels[lv]) for lv in levels}


# ---------------------------------------------------------------- css blocks


def color_block(name, ramp, prefix="brand"):
    lines = [f"  --{prefix}-{lv}: {ramp[lv]};" for lv in LEVELS]
    return "\n".join(lines)


def theme_block(mode, brand, neutral, seed):
    if mode == "light":
        return f"""  /* ---- 语义色（亮色） ---- */
  --color-bg: {neutral[50]};
  --color-surface: #ffffff;
  --color-surface-alt: {neutral[100]};
  --color-border: {neutral[200]};
  --color-border-strong: {neutral[300]};
  --color-text: {neutral[900]};
  --color-text-secondary: {neutral[600]};
  --color-text-tertiary: {neutral[500]};
  --color-primary: {brand[600]};
  --color-primary-hover: {brand[700]};
  --color-primary-active: {brand[800]};
  --color-primary-soft: {brand[50]};
  --color-on-primary: #ffffff;
  --color-focus: {brand[500]};
  --shadow-color: 15 23 42;"""
    return f"""  /* ---- 语义色（暗色，不是反色：层级越高越亮） ---- */
  --color-bg: {neutral[900]};
  --color-surface: {hsl_to_hex(hex_to_hsl(neutral[900])[0], 0.10, 0.135)};
  --color-surface-alt: {hsl_to_hex(hex_to_hsl(neutral[900])[0], 0.09, 0.185)};
  --color-border: {hsl_to_hex(hex_to_hsl(neutral[900])[0], 0.07, 0.245)};
  --color-border-strong: {hsl_to_hex(hex_to_hsl(neutral[900])[0], 0.06, 0.34)};
  --color-text: rgba(255, 255, 255, 0.87);
  --color-text-secondary: rgba(255, 255, 255, 0.60);
  --color-text-tertiary: rgba(255, 255, 255, 0.40);
  --color-primary: {brand[400]};
  --color-primary-hover: {brand[300]};
  --color-primary-active: {brand[200]};
  --color-primary-soft: {hsl_to_hex(hex_to_hsl(brand[500])[0], 0.30, 0.19)};
  --color-on-primary: {neutral[900]};
  --color-focus: {brand[400]};
  --shadow-color: 0 0 0;"""


BASE_BLOCK = """  /* ---- 间距（4pt 基数） ---- */
  --space-1: 4px;   --space-2: 8px;   --space-3: 12px;  --space-4: 16px;
  --space-6: 24px;  --space-8: 32px;  --space-12: 48px;
  --space-16: 64px; --space-24: 96px;

  /* ---- 字号（约 1.25 阶梯） ---- */
  --text-xs: 12px;   --text-sm: 14px;  --text-base: 16px; --text-lg: 18px;
  --text-xl: 20px;   --text-2xl: 24px; --text-3xl: 30px;
  --text-4xl: 36px;  --text-5xl: 48px; --text-6xl: 60px;

  /* ---- 行高 ---- */
  --leading-tight: 1.1;  --leading-snug: 1.25;
  --leading-normal: 1.5; --leading-relaxed: 1.65;

  /* ---- 字重 / 字距 ---- */
  --weight-normal: 400; --weight-medium: 500;
  --weight-semibold: 600; --weight-bold: 700;
  --tracking-tight: -0.02em; --tracking-normal: 0;
  --tracking-wide: 0.06em;

  /* ---- 圆角 ---- */
  --radius-sm: 4px; --radius-md: 8px; --radius-lg: 12px;
  --radius-xl: 16px; --radius-full: 999px;

  /* ---- 阴影（贴合层 + 氛围层） ---- */
  --shadow-0: none;
  --shadow-1: 0 1px 2px rgb(var(--shadow-color) / 0.06), 0 1px 1px rgb(var(--shadow-color) / 0.04);
  --shadow-2: 0 4px 8px -2px rgb(var(--shadow-color) / 0.08), 0 2px 4px -2px rgb(var(--shadow-color) / 0.06);
  --shadow-3: 0 12px 24px -6px rgb(var(--shadow-color) / 0.12), 0 4px 8px -4px rgb(var(--shadow-color) / 0.08);
  --shadow-4: 0 24px 48px -12px rgb(var(--shadow-color) / 0.18), 0 8px 16px -8px rgb(var(--shadow-color) / 0.10);

  /* ---- 动效 ---- */
  --ease-out: cubic-bezier(0.2, 0, 0, 1);
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
  --dur-fast: 150ms; --dur-base: 200ms; --dur-slow: 300ms;

  /* ---- 布局 ---- */
  --container: 1280px;
  --container-prose: 65ch;
  --container-form: 440px;"""

SEMANTIC_BLOCK = """  /* ---- 状态色（亮/暗通用，暗色下可再降饱和） ---- */
  --success: #15803d; --success-bg: #f0fdf4;
  --warning: #b45309; --warning-bg: #fffbeb;
  --error:   #b91c1c; --error-bg:   #fef2f2;
  --info:    #1d4ed8; --info-bg:    #eff6ff;"""


def generate(seed, mode):
    brand = make_ramp(seed)
    neutral = build_neutral(seed)
    parts = []
    parts.append("/* 由 design-quality / make_tokens.py 生成。改动请改种子色后重新生成。 */\n")
    parts.append(":root {")
    parts.append("  /* ---- 品牌色阶 ---- */")
    parts.append(color_block("brand", brand))
    parts.append("")
    parts.append("  /* ---- 中性色阶（继承品牌色相） ---- */")
    parts.append(color_block("neutral", neutral, prefix="neutral"))
    parts.append("")
    parts.append(BASE_BLOCK)
    parts.append("")
    parts.append(SEMANTIC_BLOCK)
    parts.append("")
    if mode in ("light", "both"):
        parts.append(theme_block("light", brand, neutral, seed))
    parts.append("}")
    if mode == "dark":
        parts.append("@media (prefers-color-scheme: dark) {")
    if mode == "both":
        parts.append('[data-theme="dark"] {')
    if mode in ("dark", "both"):
        parts.append(theme_block("dark", brand, neutral, seed))
        parts.append("}")
    return "\n".join(parts) + "\n"


def report(seed, mode, brand):
    out = []
    out.append(f"种子色 {seed}  →  品牌 600 = {brand[600]}")
    checks = [
        ("正文 #111827 于白底", contrast("#111827", "#ffffff"), 4.5),
        ("次级 #4b5563 于白底", contrast("#4b5563", "#ffffff"), 4.5),
        ("白字于品牌 600（主按钮）", contrast("#ffffff", brand[600]), 4.5),
        ("白字于品牌 500", contrast("#ffffff", brand[500]), 4.5),
        ("深字于品牌 50（标签底）", contrast("#111827", brand[50]), 4.5),
        ("品牌 600 于白底（链接）", contrast(brand[600], "#ffffff"), 4.5),
    ]
    out.append("")
    out.append("对比度自检：")
    for label, ratio, need in checks:
        flag = "OK " if ratio >= need else "不达标"
        out.append(f"  [{flag}] {ratio:5.2f}:1  (需 {need}:1)  {label}")
    out.append("")
    out.append("提示：主按钮用 --color-primary（=品牌 600），不要用 500；"
               "500 留给焦点环和非文字图形。")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="按种子色生成设计 token")
    ap.add_argument("--seed", default="#2563eb", help="种子色，如 #2563eb")
    ap.add_argument("--mode", default="both", choices=["light", "dark", "both"])
    ap.add_argument("--out", default="", help="输出 CSS 文件路径；不填则打印到标准输出")
    args = ap.parse_args()

    try:
        brand = make_ramp(args.seed)
        css = generate(args.seed, args.mode)
    except ValueError as e:
        print(f"错误：{e}", file=sys.stderr)
        return 2

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(css)
        print(f"已写入 {args.out}")
        print(report(args.seed, args.mode, brand))
    else:
        print(css)
        print(report(args.seed, args.mode, brand), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
