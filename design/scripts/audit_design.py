#!/usr/bin/env python3
"""HTML/CSS 设计质量审查：给出分数与硬伤清单。

用法：
    python3 audit_design.py index.html
    python3 audit_design.py ./dist            # 递归扫描 html/css
    python3 audit_design.py page.html --json

只做启发式检查，结论是线索不是判决：视觉层次、留白节奏、动效意图仍需人看。
"""

import argparse
import glob
import json
import os
import re
import sys

SPACING_SCALE = {0, 4, 8, 12, 16, 24, 32, 48, 64, 96, 128}
TYPE_SCALE = {12, 14, 16, 18, 20, 24, 30, 36, 48, 60}
RADIUS_SCALE = {0, 4, 8, 12, 16, 999}

NAMED = {"white": "#ffffff", "black": "#000000", "transparent": None}

SPACING_PROPS = ("padding", "margin", "gap", "row-gap", "column-gap",
                 "padding-top", "padding-right", "padding-bottom", "padding-left",
                 "margin-top", "margin-right", "margin-bottom", "margin-left")


# ------------------------------------------------------------------ utils


def read_text(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except OSError:
        return ""


def collect_files(target):
    if os.path.isfile(target):
        return [target]
    files = []
    for ext in ("*.html", "*.htm", "*.css"):
        for p in glob.glob(os.path.join(target, "**", ext), recursive=True):
            if "node_modules" in p or "/.git/" in p:
                continue
            files.append(p)
    return sorted(files)


def to_rgb(color):
    c = color.strip().lower()
    if c in NAMED:
        return None if NAMED[c] is None else to_rgb(NAMED[c])
    m = re.fullmatch(r"#([0-9a-f]{3}|[0-9a-f]{6})", c)
    if m:
        h = m.group(1)
        if len(h) == 3:
            h = "".join(ch * 2 for ch in h)
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    m = re.fullmatch(r"rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)(?:\s*,\s*[\d.]+)?\s*\)", c)
    if m:
        return tuple(float(x) for x in m.groups())
    return None


def luminance(rgb):
    def ch(v):
        v = float(v) / 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4

    r, g, b = rgb
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast(a, b):
    ra, rb = to_rgb(a), to_rgb(b)
    if not ra or not rb:
        return None
    la, lb = luminance(ra), luminance(rb)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def px(value, base=16.0):
    v = value.strip().lower()
    m = re.fullmatch(r"([\d.]+)px", v)
    if m:
        return float(m.group(1))
    m = re.fullmatch(r"([\d.]+)rem", v)
    if m:
        return float(m.group(1)) * base
    m = re.fullmatch(r"([\d.]+)em", v)
    if m:
        return float(m.group(1)) * base
    return None


def split_values(value):
    parts = [p.strip() for p in re.split(r"\s+", value.strip()) if p.strip()]
    out = []
    for p in parts:
        for q in p.split("/"):
            out.append(q)
    return out


# ------------------------------------------------------------------ extraction


def extract_css(sources):
    chunks = []
    for path, text in sources:
        if path.endswith(".css"):
            chunks.append(text)
            continue
        for m in re.finditer(r"<style[^>]*>(.*?)</style>", text, re.S | re.I):
            chunks.append(m.group(1))
    return "\n".join(chunks)


def extract_inline_styles(sources):
    styles = []
    for path, text in sources:
        if not path.endswith((".html", ".htm")):
            continue
        for m in re.finditer(r'style\s*=\s*"([^"]*)"', text, re.I):
            styles.append(m.group(1))
    return styles


def rules_of(css):
    css = re.sub(r"\/\*.*?\*\/", "", css, flags=re.S)
    return re.findall(r"([^{}@/][^{}]*)\{([^{}]*)\}", css)


DECL_RE = re.compile(r"([-a-zA-Z0-9_]+)\s*:\s*([^;{}]+)")  # 自定义属性 --space-4 含数字，名字要能匹配


def declarations(block):
    return [(p.strip().lower(), v.strip()) for p, v in DECL_RE.findall(block)]


# ------------------------------------------------------------------ checks


def audit_html_text(html):
    """单文件 HTML 层检查。"""
    issues = []

    no_alt = len(re.findall(r"<img\b[^>]*>", html, re.I)) - len(
        re.findall(r"<img\b[^>]*\balt\s*=", html, re.I))
    if no_alt > 0:
        issues.append((10 if no_alt >= 3 else 5, "无障碍",
                       f"{no_alt} 个 <img> 缺少 alt 属性"))
    if html and not re.search(r"<html[^>]*\blang\s*=", html, re.I):
        issues.append((4, "无障碍", "<html> 缺少 lang 声明"))
    fake_btn = len(re.findall(r'<div[^>]*class="[^"]*(btn|button)[^"]*"', html, re.I))
    if fake_btn:
        issues.append((4, "无障碍", f"{fake_btn} 处疑似用 <div> 冒充按钮，键盘不可达"))
    h1 = len(re.findall(r"<h1\b", html, re.I))
    if h1 == 0:
        issues.append((3, "结构", "页面没有 h1，标题层级缺起点"))
    elif h1 > 1:
        issues.append((4, "结构", f"{h1} 个 h1，应只有一个"))
    inline = len(re.findall(r'style\s*=\s*"', html, re.I))
    if inline > 10:
        issues.append((6, "一致性", f"{inline} 处内联样式，样式分散难以统一"))
    return issues


def audit_css(css, inline_styles):
    issues = []
    all_decls = []
    rules = rules_of(css)
    for sel, block in rules:
        for prop, val in declarations(block):
            all_decls.append((sel.strip(), prop, val))
    for style in inline_styles:
        for prop, val in declarations(style):
            all_decls.append(("inline", prop, val))

    # ---- 间距刻度
    # token 化的页面（padding: var(--space-4)）不能因为没有字面 px 就被判"未声明"，
    # 先把自定义属性里的 px 建表，再让 var(--x) 参与解析。
    custom_px = {}
    for _, prop, val in all_decls:
        if prop.startswith("--"):
            hits = re.findall(r"-?\d+\.?\d*px", val)
            if len(hits) == 1:
                custom_px[prop] = px(hits[0])

    def resolve_px(v):
        p = px(v)
        if p is not None:
            return p
        m = re.match(r"var\(\s*(--[A-Za-z0-9_-]+)", v.strip())
        if m:
            return custom_px.get(m.group(1))
        return None

    spacing_vals = []
    for _, prop, val in all_decls:
        if prop in SPACING_PROPS:
            for v in split_values(val):
                p = resolve_px(v)
                if p is not None:
                    spacing_vals.append((v, p))
    # 只有自定义属性、没有直接写在规则里的情况：用属性名带间距语义的变量来判
    if not spacing_vals:
        for name, p in custom_px.items():
            if re.search(r"(space|gap|pad|margin|inset|s\d+)", name, re.I):
                spacing_vals.append((name, p))
    if spacing_vals:
        off = [(v, p) for v, p in spacing_vals if p not in SPACING_SCALE]
        ratio = len(off) / len(spacing_vals)
        if off:
            sample = sorted({v for v, _ in off})[:6]
            issues.append((round(min(15, ratio * 30), 1), "间距",
                           f"{len(off)}/{len(spacing_vals)} 个间距值不在刻度上（示例：{'、'.join(sample)}）"))
    else:
        issues.append((6, "间距", "未检测到显式间距声明，检查是否全部内联在别处"))

    # ---- 字号
    sizes = []
    for _, prop, val in all_decls:
        if prop == "font-size":
            p = px(val)
            if p is not None:
                sizes.append(p)
    distinct = sorted(set(sizes))
    if len(distinct) > 7:
        issues.append((min(8, (len(distinct) - 6) * 2), "字体",
                       f"{len(distinct)} 种字号（{'、'.join(str(int(s)) for s in distinct[:10])}），建议压到 5–7 种"))
    elif len(distinct) < 3 and sizes:
        issues.append((3, "字体", f"只有 {len(distinct)} 种字号，字号层级偏少"))
    off_size = [s for s in distinct if s not in TYPE_SCALE]
    if len(off_size) > 1:
        issues.append((5, "字体", f"非标准字号：{'、'.join(str(int(s)) for s in off_size)}"))
    if distinct and min(distinct) < 12:
        issues.append((3, "字体", f"最小字号 {min(distinct)}px，低于 12px 可读性差"))

    # ---- 行高
    has_lh = any(p == "line-height" for _, p, _ in all_decls)
    if not has_lh and sizes:
        issues.append((6, "字体", "未设置 line-height，中文正文容易挤"))

    # ---- 颜色
    colors = set()
    for _, prop, val in all_decls:
        if prop in ("color", "background", "background-color", "border-color", "fill", "stroke"):
            for v in split_values(val):
                rgb = to_rgb(v)
                if rgb:
                    colors.add(v.strip().lower())
    if len(colors) > 20:
        issues.append((min(12, (len(colors) - 18) * 0.8), "色彩",
                       f"{len(colors)} 种颜色，缺少色板约束（建议 ≤ 18）"))

    # ---- 圆角
    radii = set()
    for _, prop, val in all_decls:
        if prop.startswith("border") and "radius" in prop:
            for v in split_values(val):
                p = px(v)
                if p is not None:
                    radii.add(p)
    if len(radii) > 4:
        issues.append((min(8, (len(radii) - 3) * 1.6), "圆角",
                       f"{len(radii)} 种圆角（{'、'.join(str(int(r)) for r in sorted(radii))}），建议 ≤ 3–4 档"))

    # ---- 对比度
    pairs, unknowns = [], 0
    for sel, block in rules:
        decl = {p: v for p, v in declarations(block)}
        fg, bg = decl.get("color"), decl.get("background-color") or decl.get("background")
        if not fg or not bg:
            continue
        if "var(" in fg or "var(" in bg or "gradient" in bg:
            unknowns += 1
            continue
        ratio = contrast(fg, bg)
        if ratio is None:
            continue
        size = px(decl.get("font-size", "16px")) or 16
        weight = int(re.sub(r"[^0-9]", "", decl.get("font-weight", "400")) or 400)
        large = size >= 18 or (size >= 14 and weight >= 700)
        pairs.append((sel, fg, bg, ratio, large, size))

    # 只声明 color、底色继承自页面：用全局底色补算，避免漏掉"浅灰正文"
    global_bg = None
    for sel, block in rules:
        if re.search(r"(^|,)\s*(body|html|:root)\s*($|,|\{)", sel, re.I):
            d = dict(declarations(block))
            cand = d.get("background-color") or d.get("background")
            if cand and to_rgb(cand):
                global_bg = cand
    assumed = global_bg is None
    bg_use = global_bg or "#ffffff"
    seen = {p[0] for p in pairs}

    # 元素自身没写底色但祖先写了（如 .cta-box 的深色卡片）时，不能拿页面底色去算，
    # 否则白字压在深色卡上会被误判成 1:1。
    bg_by_sel = {}
    for sel, block in rules:
        d = dict(declarations(block))
        b = d.get("background-color") or d.get("background")
        if b:
            bg_by_sel[sel.strip()] = b

    def ancestor_bg(sel):
        parts = [t for t in re.split(r"\s+|\>|\+|~", sel.strip()) if t]
        for i in range(len(parts) - 1, 0, -1):
            key = " ".join(parts[:i])
            if key in bg_by_sel:
                return bg_by_sel[key]
        return None

    for sel, block in rules:
        if sel in seen:
            continue
        d = dict(declarations(block))
        fg = d.get("color")
        if not fg or "var(" in fg or "background" in d or not to_rgb(fg):
            continue
        abg = ancestor_bg(sel)
        if abg and ("var(" in abg or "gradient" in abg):
            continue  # 祖先底色无法解析，不做判断
        local_bg = abg or bg_use
        rgb = to_rgb(fg)
        if assumed and not abg and luminance(rgb) > 0.65:
            continue  # 假定白底下的浅色文字，可能是深色主题，不误判
        ratio = contrast(fg, local_bg)
        if ratio is None:
            continue
        size = px(d.get("font-size", "16px")) or 16
        weight = int(re.sub(r"[^0-9]", "", d.get("font-weight", "400")) or 400)
        large = size >= 18 or (size >= 14 and weight >= 700)
        pairs.append((sel, fg, local_bg + ("(页面底色)" if (assumed and not abg) else ""), ratio, large, size))

    bad = [p for p in pairs if p[3] < (3.0 if p[4] else 4.5)]
    if bad:
        worst = sorted(bad, key=lambda x: x[3])[:3]
        detail = "；".join(f"{s[:28]} {f}/{b} = {r:.1f}:1" for s, f, b, r, _, _ in worst)
        issues.append((15 if len(bad) >= 3 else 8, "对比度",
                       f"{len(bad)} 组文字/底色对比不足 4.5:1：{detail}"))

    # ---- 焦点
    outline_off = [s for s, p, v in all_decls
                   if p == "outline" and (v.strip().lower() in ("none", "0", "0px"))]
    has_focus_rule = bool(re.search(r":focus-visible|:focus\b", css))
    if outline_off and not has_focus_rule:
        issues.append((10, "无障碍", f"{len(outline_off)} 处 outline: none 且没有 :focus-visible 替代"))

    # ---- 动效
    if "prefers-reduced-motion" not in css:
        issues.append((5, "动效", "缺少 prefers-reduced-motion 降级"))
    durations = []
    for _, prop, val in all_decls:
        if prop.startswith("transition") or prop.startswith("animation"):
            if "infinite" in val:
                continue  # 循环型动效（骨架屏 shimmer、加载指示）不受 150–300ms 区间约束
            for m in re.finditer(r"(\d+(?:\.\d+)?)(ms|s)\b", val):
                d = float(m.group(1)) * (1 if m.group(2) == "ms" else 1000)
                durations.append(d)
    durations = [d for d in durations if d >= 20]
    if durations and (min(durations) < 80 or max(durations) > 600):
        issues.append((4, "动效",
                       f"动效时长跨度 {min(durations):.0f}–{max(durations):.0f}ms，建议集中在 150–300ms"))

    # ---- 版式宽度
    if not re.search(r"max-width|clamp\(|ch\b|--container", css):
        issues.append((7, "版式", "没有任何 max-width / ch 限制，长行会破坏阅读"))
    if not re.search(r"grid|flex", css):
        issues.append((4, "版式", "未检测到 grid/flex 布局"))

    return issues


def run(target):
    files = collect_files(target)
    if not files:
        print(f"未找到 html/css 文件：{target}", file=sys.stderr)
        return 2
    sources = [(f, read_text(f)) for f in files]
    html_sources = [(f, t) for f, t in sources if f.endswith((".html", ".htm"))]
    css = extract_css(sources)
    inline = extract_inline_styles(sources)

    issues = []
    if len(html_sources) == 1:
        issues += audit_html_text(html_sources[0][1])
    else:
        # 多文件：只在"所有文件都有同类问题"时按文件数轻度累加，避免误判
        buckets = {}
        for f, t in html_sources:
            for w, dim, msg in audit_html_text(t):
                key = msg.split("，")[0].split(" ")[0]
                buckets.setdefault(key, [0, w, dim, msg])
                buckets[key][0] += 1
        for key, (cnt, w, dim, msg) in buckets.items():
            heavy = any(k in key for k in ("h1", "alt", "lang", "outline", "内联"))
            if cnt > 1 or len(html_sources) == 1:
                issues.append((min(w * 2, 12) if heavy else w, dim,
                               f"{cnt}/{len(html_sources)} 个文件：{msg}"))
    issues += audit_css(css, inline)

    issues = [(round(w, 1), d, m) for w, d, m in issues]
    score = max(0.0, 100.0 - sum(w for w, _, _ in issues))
    view = "可交付" if score >= 80 else ("需修结构" if score >= 60 else "建议重做")
    return {
        "target": target,
        "files": len(files),
        "score": round(score, 1),
        "verdict": view,
        "issues": [{"deduct": w, "dimension": d, "detail": m} for w, d, m in issues],
    }


DIM_ORDER = ["结构", "版式", "间距", "字体", "色彩", "圆角", "对比度", "无障碍", "动效", "一致性"]


def render(res):
    lines = []
    lines.append(f"设计审查 · {os.path.basename(os.path.abspath(res['target']))}（{res['files']} 个文件）")
    if res["files"] > 1:
        lines.append("（多文件为合并统计；单页问题请逐个文件运行）")
    lines.append("")
    grade = ("A" if res["score"] >= 90 else "B" if res["score"] >= 80 else
             "C" if res["score"] >= 70 else "D" if res["score"] >= 60 else "F")
    lines.append(f"分数：{res['score']}/100  等级 {grade}")
    lines.append("")
    if not res["issues"]:
        lines.append("没有检出硬伤。仍需人工确认：模糊测试、灰度测试、键盘走查。")
    else:
        lines.append("问题清单（按维度，数字为扣分）：")
        for d in DIM_ORDER:
            group = [i for i in res["issues"] if i["dimension"] == d]
            for i in group:
                lines.append(f"  [{d}] -{i['deduct']}  {i['detail']}")
        total = sum(i["deduct"] for i in res["issues"])
        lines.append("")
        lines.append(f"合计扣分 {total:.1f}。修复顺序：结构 → 版式/间距 → 字体/色彩 → 对比度/无障碍 → 动效与细节。")
    lines.append("")
    lines.append("注：变量（var(--x)）、渐变、图片背景无法计算对比度，已跳过；"
                 "本工具覆盖约 40% 的可见问题，层次与留白仍需人眼判断。")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="HTML/CSS 设计质量审查")
    ap.add_argument("target", help="html/css 文件或目录")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    res = run(args.target)
    if isinstance(res, int):
        return res
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print(render(res))
    return 0


if __name__ == "__main__":
    sys.exit(main())
