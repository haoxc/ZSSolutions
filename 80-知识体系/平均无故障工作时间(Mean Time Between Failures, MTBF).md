---
aliases:
  - Mean Time Between Failures
  - MTBF
  - 平均无故障工作时间
  - sy:MTBF 平均无故障工作时间
title: 平均无故障工作时间(Mean Time Between Failures, MTBF)
tags:
  - 知识体系
  - 术语
  - 可靠性
  - 系统设计
description: >
  MTBF 是系统或组件在两次故障之间的平均运行时间，用于量化可靠性。不同于可用性百分比，MTBF 是统计值而非瞬时值。
type: term
create-date: 2026-06-19
---

# 平均无故障工作时间 (MTBF)

> MTBF = 总运行时间 / 故障次数。单位通常为小时。值越高系统越可靠。

## 核心要点

- **整站指标，非单组件**：允许单组件故障，但系统整体持续运行。单台服务器的故障不应导致系统级 MTBF 统计归零。
- **统计周期**：MTBF 需长期统计才有意义。10,000h ≈ 1.14 年连续运行——无法在交付时验收，只能在质保期内持续统计。
- **与可用性的关系**：MTBF 和可用性（Availability = MTBF/(MTBF+MTTR)）是不同维度。MTBF 管故障间隔，MTTR 管修复速度。两者共同决定可用性。

## 常见误区

| 误区 | 实际 |
|------|------|
| MTBF = 寿命 | MTBF 是故障间隔，产品寿命可以远长于 MTBF |
| MTBF 10000h = 每台设备都能跑 10000h | MTBF 是统计均值，个别设备可能更早故障 |
| 99.99% 可用性 = MTBF 达标 | 四九可用性（年停机 52min）靠高 MTBF + 低 MTTR 共同实现 |

## 相关

- JBFG 非功能指标 P18：MTBF ≥10,000h（→ [[非功能指标定义]]）
- JBFG 方案书 5.2 可靠性设计（→ [[冀北风光储数智化生产支撑与数字孪生解决方案-大纲(v1)]]）
- RB5 风险：MTBF 验收周期不可行 → 质保期内持续统计，期末达标

## 参考

- MIL-HDBK-217F, Reliability Prediction of Electronic Equipment
- IEC 60050-192, International Electrotechnical Vocabulary — Dependability
