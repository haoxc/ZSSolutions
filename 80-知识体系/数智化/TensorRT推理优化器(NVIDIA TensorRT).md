---
aliases: [TensorRT, NVIDIA TensorRT, TensorRT 推理优化器]
tags: [知识体系, 数智化, AI, 推理优化, GPU 加速]
description: NVIDIA TensorRT 是 NVIDIA 推出的深度学习推理优化 SDK，通过量化、层融合、内核自动调优等技术加速 AI 模型在 GPU 上的部署
type: 概念定义
create-date: 2026-06-19
---

# TensorRT 推理优化器

## 一句话定义

**NVIDIA TensorRT** 是 NVIDIA 推出的**深度学习推理优化 SDK**，对训练好的模型（以 ONNX 为主导入格式）执行**量化（FP8/INT8/INT4）、层融合、内核自动调优**等优化，生成针对特定 GPU 架构的高效推理引擎，实现低延迟、高吞吐的 AI 模型生产部署。官方地址：`developer.nvidia.com/tensorrt`。

## 最小理解图

```
训练完成                          TensorRT 优化                         部署
┌─────────┐    ONNX 模型    ┌─────────────────┐    优化后引擎    ┌──────────┐
│ PyTorch │───→ .onnx ─────→│ 精度校准 (INT8)  │───→ .engine ──→│ H100     │
├─────────┤                 │ 层融合            │                │ A100     │
│ TF      │                 │ 内核自动调优        │                │ RTX 5090 │
├─────────┤                 │ CUDA Graph       │                │ Jetson   │
│ Other   │                 │ 动态形状处理       │                │ DRIVE    │
└─────────┘                 └─────────────────┘                └──────────┘
```

## 优化技术栈

| 技术 | 说明 | 效果 |
|------|------|------|
| **量化** | FP32/BF16/FP8/INT8/INT4 精度降低，TL:FP16→INT8 压缩 | 吞吐 2-4×，显存减半 |
| **层融合** | 相邻算子合并减少 kernel 启动开销 | 启动开销从 5-15µs/op 归零 |
| **内核自动调优** | 为每层每硬件自动选择最快 kernel | 硬件利用率最大化 |
| **CUDA Graph** | 捕获整个推理图为单次 launch | 消除每 kernel 调度延迟 |
| **结构化稀疏 (2:4)** | Ampere+ 架构的 50% 权重置零加速 | 额外 1.62× 加速 |

## 生态组件

| 组件 | 定位 | 适用场景 |
|------|------|---------|
| **TensorRT Core** | 通用推理编译器 + 运行时 | 标准 CV/NLP 模型 GPU 部署 |
| **TensorRT-LLM** | LLM 专用推理库 | 大语言模型（Llama/GPT/Qwen）推理加速 |
| **TensorRT Model Optimizer** | 模型压缩工具（量化/剪枝/蒸馏） | 部署前精度→性能权衡 |
| **TensorRT for RTX** | < 200MB 轻量 JIT 推理库 | RTX 桌面端应用（SD/ComfyUI） |
| **Torch-TensorRT** | PyTorch 编译后端 | 一行代码集成 PyTorch 推理优化 |

## 容易混淆

| 概念 | 与 TensorRT 的区别 |
|------|-------------------|
| **ONNX** | ONNX 是**模型交换格式**，TensorRT 是**推理优化引擎**。ONNX 为 TensorRT 提供输入，两者是上下游而非竞争关系 |
| **OpenVINO** | Intel 的推理优化工具，优化 Intel CPU/GPU/VPU。TensorRT 只优化 NVIDIA GPU，两者服务于不同硬件生态 |
| **vLLM** | vLLM 专注 LLM 推理的**内存管理**（PagedAttention + 连续批处理），TensorRT-LLM 是端到端的**编译优化 + 运行时**。两者在 LLM 场景有功能重叠 |

## 典型例子

```python
# PyTorch → ONNX → TensorRT 推理
import torch
import tensorrt as trt

# 1. ONNX 导出
torch.onnx.export(model, dummy, "model.onnx")

# 2. TensorRT 构建引擎
logger = trt.Logger(trt.Logger.WARNING)
builder = trt.Builder(logger)
network = builder.create_network()
parser = trt.OnnxParser(network, logger)
parser.parse_from_file("model.onnx")

config = builder.create_builder_config()
config.set_memory_pool_limit(trt.MemoryPoolType.WORKSPACE, 1 << 30)  # 1GB
config.set_flag(trt.BuilderFlag.FP16)          # FP16 量化

engine = builder.build_serialized_network(network, config)
with open("model.engine", "wb") as f:
    f.write(engine)
```

**典型链路**：
- CV 模型：PyTorch → ONNX → TensorRT → NVIDIA GPU 实时推理
- LLM 部署：PyTorch FSDP 训练 → TensorRT-LLM FP8 量化 → 单 H100 高吞吐服务
- 桌面应用：Stable Diffusion → TensorRT for RTX JIT 编译 → ComfyUI 即时出图

## 性能示例

| 模型 | 优化 | 加速比 |
|------|------|--------|
| Llama 2 70B | FP8 + 稀疏化 (batch=32) | 1.62× over FP8 dense |
| SDXL | INT8 PTQ on RTX 6000 Ada | 1.43× over FP16 |
| FLUX.1 | RTX 5090 自适应推理 | 1.32× over 静态优化 |
| Falcon 180B | INT4 AWQ | 单卡 H200 可部署 |

## 压缩记忆

> **TensorRT = 模型部署前的性能打磨：量化 + 融合 + 调优 + CUDA Graph，一套优化通吃所有 GPU**

## 参考来源

- [NVIDIA TensorRT Developer Page](https://developer.nvidia.com/tensorrt)
- [NVIDIA TensorRT Documentation (v11.0)](https://docs.nvidia.com/deeplearning/tensorrt/latest/index.html)
- [NVIDIA TensorRT-LLM GitHub](https://github.com/NVIDIA/TensorRT-LLM)
