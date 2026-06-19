---
aliases: [COLA, Clean Object-oriented & Layered Architecture, 可乐架构]
tags: [知识体系, 数智化, 软件架构, 应用架构]
description: COLA（Clean Object-oriented & Layered Architecture）是阿里巴巴开源的 Java 应用架构框架，提供可复制的分层规范和工程化实践
type: 概念定义
create-date: 2026-06-19
---

# COLA 架构

## 一句话定义

**COLA（Clean Object-oriented & Layered Architecture，可乐架构）** 是阿里巴巴开源的 Java 应用架构框架，旨在提供一套**可复制的、易读的、可落地的**架构规范，通过显式分层和依赖倒置控制应用复杂度、延缓系统腐化。开源地址：`github.com/alibaba/COLA`（12.9k+ stars）。

## 最小理解图

```
┌──────────────────────────────────────┐
│          Adapter Layer (适配层)         │  ← 处理外部请求（Web/WAP/API），等同 Controller
├──────────────────────────────────────┤
│          Client Layer (客户端层)        │  ← 对外暴露服务接口 & DTO
├──────────────────────────────────────┤
│        Application Layer (应用层)       │  ← 用例编排、参数校验、事务管理（不含业务规则）
├──────────────────────────────────────┤
│         Domain Layer (领域层)           │  ← 核心业务逻辑：Entity、Domain Service、Gateway 接口
├──────────────────────────────────────┤
│      Infrastructure Layer (基础设施层)    │  ← 数据库 CRUD、RPC、MQ、Gateway 实现
└──────────────────────────────────────┘
```

核心关系：领域层定义 **Gateway 接口** → 基础设施层实现 → 领域层不直接依赖任何基础设施技术。

## 判断标准

使用 COLA 架构的项目应满足以下特征：

| 维度 | 判断标准 |
|------|---------|
| **分包** | 顶层按业务领域分包（如 `customer/`、`order/`），不按技术功能分包 |
| **依赖** | 领域层通过 Gateway 接口反向依赖基础设施层（依赖倒置） |
| **应用层** | 只做**编排不做业务规则**，不包含 Entity 或领域逻辑 |
| **DTO/异常** | 使用标准化 DTO、BizException/SysException 层次 |
| **扩展点** | 多业务线共存时使用 Extension 机制而非 if-else |

## 容易混淆

| 概念 | 与 COLA 的区别 |
|------|---------------|
| **DDD（领域驱动设计）** | COLA 吸收了 DDD 的分层思想，但不是完整 DDD 方法论。COLA 更关注**落地实践**和**工程化约束**，不强制使用 Event Sourcing、Aggregate 等 DDD 战术模式 |
| **Clean Architecture** | COLA 受 Robert Martin 的 Clean Architecture 启发，但增加了 Java/Spring 生态的具体实现（如 Spring Boot starter、MyBatis 集成）、扩展点机制、状态机组件 |
| **MVC** | COLA 包含 Controller（Adapter）层，但增加了显式的 Application 层（编排）+ Domain 层（业务规则）+ Infrastructure 层（技术实现），**三层 vs MVC 的两层** |
| **普通分层架构** | 普通分层往往是"Controller → Service → DAO"，领域逻辑散落在 Service 中。COLA 强制将业务规则**显式放入 Domain 层**，Service 退化为编排器 |

## 典型例子

电商订单系统的 COLA 包结构：

```
com.company.order/
├── adapter/          ← Web 接口、消息监听
├── client/           ← OrderDTO、OrderService 接口
├── app/              ← CreateOrderAppService（编排校验→领域调用→持久化）
├── domain/           ← OrderEntity、OrderGateway 接口
├── infrastructure/   ← OrderGatewayImpl（MyBatis/Redis）
└── start/            ← Spring Boot 启动类
```

订单创建流程：Adapter 接收请求 → AppService 参数校验 → DomainEntity 执行业务规则 → Gateway 持久化。

## 关键组件（COLA 5.0）

| 组件 | 功能 |
|------|------|
| `cola-component-dto` | 标准化 DTO/响应格式、分页 |
| `cola-component-exception` | BizException & SysException 异常层次 |
| `cola-component-statemachine` | 轻量状态机引擎 |
| `cola-component-domain-starter` | Spring 管理的领域实体 |
| `cola-component-extension-starter` | 运行时扩展点（多业务线支持） |
| `cola-component-catchlog-starter` | 异常拦截与日志 |

## 压缩记忆

> **可乐架构 = 领域分包 + 依赖倒置网关 + 应用编排层 + 扩展点**

六个字："**分**（领域分包）**倒**（依赖倒置）**编**（应用编排）**扩**（扩展点）**标**（标准化 DTO/异常）**启**（Spring Boot starter）"。

## 参考来源

- [alibaba/COLA GitHub](https://github.com/alibaba/COLA)
- [The Simplicity of COLA — Alibaba Cloud Blog](https://www.alibabacloud.com/blog/the-simplicity-of-cola-an-alibaba-open-source-application-architecture_597234)
