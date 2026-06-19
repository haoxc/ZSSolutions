---
aliases: [GOOSE, Generic Object Oriented Substation Event, IEC 61850 GOOSE]
tags: [知识体系, 风光储, IEC61850, 通信协议, 变电站自动化]
description: GOOSE（Generic Object Oriented Substation Event）是 IEC 61850 标准中定义的变电站高速通信协议，以发布-订阅模式替代传统硬接线
type: 概念定义
create-date: 2026-06-19
---

# GOOSE 协议

## 一句话定义

**GOOSE（Generic Object Oriented Substation Event）** 是 IEC 61850 标准中定义的通用面向对象变电站事件通信协议，用于变电站/新能源场站内**智能电子设备（IED）之间的高速实时信号交换**，以发布-订阅组播模式替代传统点对点硬接线，典型传输延迟小于 4ms。

## 最小理解图

```
  Publisher (保护 IED)                    Subscribers (断路器 IED, 录波器, ...)
       │                                        ▲
       │  GOOSE 组播 (EtherType 0x88B8)          │
       │  ┌──────────────────────────────┐       │
       │  │ 状态位 │ 模拟值 │ 时间戳 │ 质量位 │       │
       │  └──────────────────────────────┘       │
       │────────────────────────────────────────>│
       │    ① 稳态：T0 间隔发送心跳                │
       │    ② 事件：立即发送 + 逐次递增间隔重传       │
       │    ③ 接收端：超时未收到 → 宣告通信中断      │
       ▼
  持续监视链路状态（硬接线做不到）
```

| 特性 | 说明 |
|------|------|
| **通信模型** | 发布-订阅（Publisher-Subscriber），无连接组播 |
| **网络层** | 直接映射到以太网链路层（Layer 2），绕过 TCP/IP |
| **EtherType** | `0x88B8` |
| **传输性能** | 跳闸类 ≤ 3ms（P2/P3），连锁 ≤ 20ms（P1） |
| **可靠性** | 心跳（T0）+ 事件触发递增重传（2ms→4ms→8ms…） |

## 核心机制

### 重传机制（关键可靠性设计）

GOOSE 不使用 ACK 确认。可靠性通过以下时序保证：

1. **稳态（Steady State）**：以 `T0` 间隔（如 1-5s）持续发送心跳消息，持续监视通信链路
2. **事件（Event）**：数据集值变化时**立即发送**新消息
3. **Burst 重传**：以递增间隔（2ms → 4ms → 8ms → …）连续重传，直到恢复稳态 T0
4. **超时检测**：接收端维护 `timeAllowedToLive` 计时器，超时未收到有效消息 → 宣告通信中断

### 与硬接线对比

| 维度 | 硬接线 | GOOSE |
|------|--------|-------|
| 布线 | 每信号一对铜缆 | 单根以太网线，所有信号共享 |
| 扩展 | 需新增电缆和 I/O 触点 | 软件配置变更即可 |
| 监视 | 无法区分"无信号"和"断线" | 心跳提供连续链路监视 |
| 数据量 | 仅二进制通断 | 二进制 + 模拟值 + 时间戳 + 质量位 |
| 自描述 | 需查图纸/对照表 | 保留完整 IEC 61850 路径名 |

## 容易混淆

| 概念 | 与 GOOSE 的区别 |
|------|----------------|
| **MMS（Manufacturing Message Specification）** | MMS 是客户端-服务器（请求-响应）模型，走 TCP/IP，用于参数读写、控制、报告；GOOSE 是发布-订阅（组播），走 Layer 2，用于高速事件信号 |
| **SV（Sampled Values, IEC 61850-9-2）** | SV 传输**采样值**（电流/电压波形数据），GOOSE 传输**状态/事件信号**（跳闸、位置、告警）。SV 数据量大且持续发送，GOOSE 事件驱动 |
| **传统硬接线** | 硬接线是点对点物理连接，GOOSE 是以太网组播。GOOSE 增加自描述、心跳监视、灵活配置，但引入了网络安全风险（IEC 62351） |

## 典型例子

**断路器跳闸场景**：

1. 保护 IED 检测到线路故障电流
2. 保护 IED 通过 GOOSE 发送跳闸命令（数据集中 BreakerPos=TRIP）
3. 断路器 IED 接收 GOOSE 消息，在 **< 4ms** 内执行跳闸
4. 断路器 IED 通过 GOOSE 返回状态变化（BreakerPos=OPEN）
5. 所有订阅该信号的 IED（录波器、监控系统、其他保护）同步收到状态更新

若使用硬接线：需要从保护 IED 到每个接收设备各拉一对电缆，无法监视链路完整性。

## 安全注意事项（IEC 62351）

GOOSE 原设计假设在**物理隔离**的变电站网络内运行。接入外部网络时需补充安全措施：

- **认证**：数字签名验证消息来源
- **完整性**：CRC 校验（Edition 2.1 强制的）
- **防重放**：通过 `stNum`/`sqNum` 序列号检测
- **加密**：通常**不使用**（加密引入延迟会突破 3-4ms 时限）

## 压缩记忆

> **GOOSE = 变电站以太网替代硬接线，发布订阅 + 心跳监视 + 事件递增重传，4ms 内可靠送达**

## 参考来源

- [IEC 61850 GOOSE — iGrid Smart Guide](https://www.igrid-td.com/smartguide/iec61850/goose-messaging/)
- [Generic Substation Events — Wikipedia](https://en.wikipedia.org/wiki/Generic_Substation_Events)
- [GOOSE Message Applications — IET](https://digital-library.theiet.org/doi/10.1049/etr.2016.0100)
