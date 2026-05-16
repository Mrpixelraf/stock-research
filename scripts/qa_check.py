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
    rt = sorted(set(re.findall(r"RT-\d+", text)))
    modules = sorted(set(re.findall(r"M-\d+", text)))
    xml = len(re.findall(r"```xml", text))

    expect_rt = {f"RT-{i:02d}" for i in range(1, 16)}
    missing_rt = sorted(expect_rt - set(rt))
    expect_m = {f"M-{i:02d}" for i in range(1, 12)}
    missing_m = sorted(expect_m - set(modules))

    print(f"报告: {path}\n" + "-" * 50)
    print(f"中文字数      : {cn:>6}   目标 15000   {'✅' if cn >= 13000 else '⚠️ 偏少'}")
    print(f"红队节点 RT   : {len(rt):>6}/15      {'✅' if not missing_rt else '❌ 缺 ' + ','.join(missing_rt)}")
    print(f"模块 M-       : {len(modules):>6}/11      {'✅' if not missing_m else '❌ 缺 ' + ','.join(missing_m)}")
    print(f"XML schema    : {xml:>6}/5       {'✅' if xml >= 5 else '❌ 不足'}")

    ok = cn >= 13000 and not missing_rt and not missing_m and xml >= 5
    print("-" * 50)
    print("✅ 质检通过" if ok else "⚠️  未达标，回 Phase 2 补全")
    return 0 if ok else 2


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python3 qa_check.py <报告.md 路径>")
        sys.exit(1)
    sys.exit(check(sys.argv[1]))
