#!/usr/bin/env python3
"""Phase 3 质检 —— 校验 v3.1 深度分析报告的结构完整性。

用法: python3 qa_check.py <报告.md 路径>
"""
import re
import sys


def check(path: str) -> int:
    try:
        text = open(path, encoding="utf-8").read()
    except OSError as e:
        print(f"❌ 无法读取: {e}")
        return 1

    cn = len(re.findall(r"[一-鿿]", text))
    modules = sorted(set(re.findall(r"M-\d+", text)))
    xml = len(re.findall(r"```xml", text))
    debates = len(re.findall(r"^#{2,4}\s*争议", text, re.MULTILINE))
    has_kd = "核心争议与反方观点" in text
    has_catalyst = "催化剂日历" in text

    expect_m = {f"M-{i:02d}" for i in range(1, 12)}
    missing_m = sorted(expect_m - set(modules))
    kd_ok = has_kd and debates >= 5
    legacy_rt = len(re.findall(r"🔴\s*\*\*RT-\d+", text))

    print(f"报告: {path}\n" + "-" * 50)
    print(f"中文字数      : {cn:>6}   （参考值，不作硬门槛——结构完整优先）")
    print(f"核心争议专章  : {debates:>6} 条争议    {'✅' if kd_ok else '❌ 缺专章或争议 < 5'}")
    print(f"模块 M-       : {len(modules):>6}/11      {'✅' if not missing_m else '❌ 缺 ' + ','.join(missing_m)}")
    print(f"XML schema    : {xml:>6}/5       {'✅' if xml >= 5 else '❌ 不足'}")
    print(f"催化剂日历     : {'  含 ✅' if has_catalyst else '  缺 ❌ GS 四段式必含'}")
    if legacy_rt:
        print(f"⚠️  检出 {legacy_rt} 个内联 🔴RT-XX 红框——v3.1 已弃用，应融入正文 + 收口核心争议专章")

    ok = not missing_m and xml >= 5 and kd_ok and has_catalyst and not legacy_rt
    print("-" * 50)
    print("✅ 质检通过" if ok else "⚠️  未达标，回 Phase 2 补全")
    return 0 if ok else 2


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python3 qa_check.py <报告.md 路径>")
        sys.exit(1)
    sys.exit(check(sys.argv[1]))
