---
aliases: [PyTorch, PyTorch 深度学习框架, PyTorch 框架]
tags: [知识体系, 数智化, AI, 深度学习框架, 机器学习]
description: PyTorch 是 Meta AI 发起、PyTorch Foundation 托管的开源深度学习框架，以动态计算图和自动微分为核心，为 AI 研究和生产提供灵活高效的开发体验
type: 概念定义
create-date: 2026-06-19
---

# PyTorch 框架

## 一句话定义

**PyTorch** 是 Meta AI 发起（现由 Linux Foundation 旗下的 PyTorch Foundation 托管）的**开源深度学习框架**，以**动态计算图（Eager Execution）**、**自动微分（Autograd）**和**GPU 加速张量计算**为核心，兼顾研究灵活性与生产部署效率。NeurIPS 2024 中 75% 的论文使用 PyTorch。官方地址：`pytorch.org`。

## 最小理解图

```
PyTorch 能力层次
┌─────────────────────────────────────┐
│  应用层：torchvision / torchaudio    │
│           Hugging Face / Lightning   │
├─────────────────────────────────────┤
│  模型层：torch.nn / torch.optim      │
│           module / loss / optimizer  │
├─────────────────────────────────────┤
│  自动微分层：torch.autograd           │
│            DAG 构建 + 反向传播        │
├─────────────────────────────────────┤
│  编译栈：torch.compile                │
│   TorchDynamo→AOTAutograd→Inductor  │
├─────────────────────────────────────┤
│  张量层：torch.Tensor                │
│   GPU 加速 (CUDA/MPS/ROCm/XPU)     │
└─────────────────────────────────────┘
```

## 核心特性

| 特性 | 说明 |
|------|------|
| **动态计算图** | "Define-by-run"——图在执行时动态构建，Python 控制流（`if`/`for`）直接可用，调试零门槛 |
| **Autograd** | 磁带式自动微分，运行时记录操作构建 DAG，自动计算梯度 |
| **torch.compile** | PyTorch 2.x 编译栈，将 Python 级 JIT 捕获的图编译为高效 GPU kernel（均值加速 ~43%） |
| **分布式训练** | FSDP（大模型分片并行）、DeviceMesh（多维拓扑）、Tensor Parallelism |
| **多硬件支持** | NVIDIA CUDA、AMD ROCm、Intel XPU、Apple MPS、Google TPU |

**torch.compile 四层架构**：

| 组件 | 作用 |
|------|------|
| TorchDynamo | Python 级 JIT，通过帧评估钩子捕获计算图（99% 成功率） |
| AOTAutograd | 提前追踪反向传播图 |
| PrimTorch | 将约 2000 个算子标准化为约 250 个原语 |
| TorchInductor | 代码生成——GPU 生成 Triton kernel，CPU 生成 C++ |

## 容易混淆

| 概念 | 与 PyTorch 的区别 |
|------|------------------|
| **TensorFlow** | TF 2.x 虽已引入 Eager 模式，但设计哲学不同：TF 偏向生产级静态图 + 服务生态（TF Serving），PyTorch 以研究灵活性见长。PyTorch 社区在学术界占主导地位 |
| **JAX** | JAX 面向函数式变换（`grad`/`jit`/`vmap`/`pmap`），追求纯函数和 XLA 编译；PyTorch 面向命令式研究和完整生态，上手更直观 |
| **ONNX** | ONNX 是模型交换**格式标准**，PyTorch 是训练**框架**。两者互补：PyTorch 训练 → ONNX 导出 → 跨平台部署 |

## 典型例子

```python
# 定义模型
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(784, 10)
    def forward(self, x):
        return self.fc(x.view(x.size(0), -1))

# 训练循环
model = Net().to("cuda")
loss_fn = nn.CrossEntropyLoss()
opt = torch.optim.Adam(model.parameters())

for data, target in dataloader:
    opt.zero_grad()
    out = model(data.to("cuda"))
    loss = loss_fn(out, target.to("cuda"))
    loss.backward()
    opt.step()
```

**常见落地链路**：
- 研究：PyTorch 动态图实验 → torch.compile 加速 → ONNX/TensorRT 部署
- 大模型：FSDP 分布式训练 → TensorRT-LLM 推理优化
- 边缘：torch.export → ExecuTorch 移动端推理

## 压缩记忆

> **PyTorch = 动态图研究 + torch.compile 生产 + Autograd 自动微分 + 多硬件 GPU**

## 参考来源

- [PyTorch Official Documentation](https://pytorch.org/docs/stable/)
- [PyTorch Overview — NVIDIA Docs](https://docs.nvidia.com/deeplearning/frameworks/pytorch-release-notes/overview.html)
- [What is PyTorch? — NVIDIA Glossary](https://www.nvidia.com/en-eu/glossary/pytorch/)
