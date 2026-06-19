---
aliases: [ONNX, Open Neural Network Exchange, ONNX 格式]
tags: [知识体系, 数智化, AI, 模型格式, 模型部署]
description: ONNX（Open Neural Network Exchange）是微软发起、业界广泛支持的开放神经网络交换格式，实现 AI 模型在不同框架和硬件间的互操作
type: 概念定义
create-date: 2026-06-19
---

# ONNX 开放格式

## 一句话定义

**ONNX（Open Neural Network Exchange）** 是微软于 2017 年发起的开放神经网络交换格式标准，定义了一套**框架无关的模型中间表示（IR）**，使 PyTorch/TensorFlow 等不同框架训练的 AI 模型能够在不同运行时和硬件之间互操作。官方地址：`onnx.ai` / `github.com/onnx/onnx`。

## 最小理解图

```
训练框架                         部署目标
┌─────────┐   ONNX 模型 (.onnx)   ┌───────────┐
│ PyTorch │─────→ 计算图 IR ─────→│ ONNX      │
├─────────┤    (Protobuf 序列化)   │ Runtime   │──→ CPU/GPU/NPU
│ TF/Keras│─────→               ├───────────┤
├─────────┤                      │ TensorRT  │──→ NVIDIA GPU
│ Scikit- │                      ├───────────┤
│ learn   │─────→               │ OpenVINO  │──→ Intel CPU/VPU
├─────────┤                      ├───────────┤
│ HugFace │                      │ CoreML    │──→ Apple Silicon
└─────────┘                      └───────────┘
```

核心价值：**一次导出，多处运行**——训练和部署解耦，不再绑定框架生态。

## 判断标准

一个模型格式是否属于 ONNX 生态的典型特征：

| 维度        | 标志                                                                    |
| --------- | --------------------------------------------------------------------- |
| **开放标准**  | 由 Linux Foundation AI 托管，非单一厂商控制                                      |
| **IR 定义** | 使用 Protocol Buffers 序列化计算图（`ModelProto` → `GraphProto` → `NodeProto`） |
| **算子集**   | 标准算子库（`ai.onnx` 域），版本化管理                                              |
| **执行提供者** | 通过 Execution Provider 机制支持多硬件后端                                       |
| **两种变体**  | ONNX（神经网络）和 ONNX-ML（含传统 ML 算法如 SVM、Tree）                              |
|           |                                                                       |

## 容易混淆

| 概念                          | 与 ONNX 的区别                                                                 |
| --------------------------- | -------------------------------------------------------------------------- |
| **PyTorch/TensorFlow 原生格式** | 原生格式绑定框架运行时，ONNX 是**框架中立**的中间表示。原生格式用于训练，ONNX 用于部署                         |
| **TensorRT**                | TensorRT 是 NVIDIA 的**推理优化引擎**，以 ONNX 为输入格式之一；ONNX 是模型表示标准，TensorRT 是优化推理工具 |
| **OpenVINO**                | Intel 的推理优化工具，也支持导入 ONNX；两者是**互补**关系而非竞争                                   |
| **TorchScript**             | PyTorch 的序列化格式，仅限 PyTorch 生态；ONNX 是跨框架标准                                   |

## 典型例子

**模型流转链路**：PyTorch 训练 → ONNX 导出 → TensorRT 优化 → NVIDIA GPU 部署

```python
# PyTorch → ONNX 导出
import torch
model = torch.load("model.pth")
dummy = torch.randn(1, 3, 224, 224)
torch.onnx.export(model, dummy, "model.onnx",
                  input_names=["input"],
                  output_names=["output"],
                  dynamic_axes={"input": {0: "batch_size"}})

# ONNX Runtime 推理
import onnxruntime as ort
session = ort.InferenceSession("model.onnx")
result = session.run(None, {"input": input_data})
```

**常见落地场景**：
- 云端：PyTorch 训练 → ONNX → TensorRT 加速推理
- 边缘：训练 → ONNX → ONNX Runtime Mobile 离线推理
- Web 端：ONNX Runtime Web（WebGL/WebAssembly）

## 关键优势

| 优势       | 说明                                                  |     |
| -------- | --------------------------------------------------- | --- |
| **框架解耦** | 训练框架和部署运行时独立选择，不绑定单一厂商                              |     |
| **硬件适配** | 同一 `.onnx` 文件通过不同 Execution Provider 适配 CPU/GPU/NPU |     |
| **图优化**  | ONNX Runtime 自动执行算子融合、常量折叠、量化等优化                    |     |
| **双版本**  | 支持 ONNX-ML（含传统 ML 算法）覆盖完整 ML 场景                     |     |

## 压缩记忆

> **ONNX = AI 模型的标准集装箱，一次打包、任意平台卸货**

## 参考来源

- [ONNX GitHub Repository](https://github.com/onnx/onnx)
- [ONNX Intermediate Representation Specification](https://onnx.ai/onnx/repo-docs/IR.html)
- [Ultralytics ONNX Glossary](https://www.ultralytics.com/glossary/onnx-open-neural-network-exchange)
