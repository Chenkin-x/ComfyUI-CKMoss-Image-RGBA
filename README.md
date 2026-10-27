<p align="center"><img src="assets/banner.png" alt="CKMoss Image RGBA" width="100%"></p>

<p align="center"><b>让角色、插画和小物件，自由进入你的画面。</b></p>
<p align="center">中文 · <a href="README.en.md">English</a> · <a href="https://huggingface.co/ChenkinLab/CKMoss-Image-RGBA">模型下载</a> · <a href="https://github.com/Chenkin-x/CKMoss-Image-RGBA">模型代码</a></p>
<p align="center">作者：<a href="https://github.com/chinoll">chinoll</a></p>

为 MOSS-Image 添加 RGBA 图像输出，直接保存带 Alpha 通道的 PNG。节点沿用 ComfyUI 的模型加载、文本提示和采样工作流。

**不用 DiT LoRA 也能生成图片。** 保留原版 MOSS-Image，加载本项目的 RGBA VAE 即可；DiT LoRA 是可选的透明图像适配组件。两种用法都附有工作流，透明背景和边缘表现会随提示词与组合变化。

## 安装

1. 更新 ComfyUI，并按 [MOSS-Image 官方说明](https://github.com/OpenMOSS/MOSS-Image/blob/main/comfyui/README.md)准备基础模型和文本编码器。
2. 将本仓库克隆到 `ComfyUI/custom_nodes/`：

   ```bash
   cd ComfyUI/custom_nodes
   git clone https://github.com/Chenkin-x/ComfyUI-CKMoss-Image-RGBA.git
   ```

3. 重启 ComfyUI。此节点包没有额外的 Python 依赖。

目录应为 `ComfyUI/custom_nodes/ComfyUI-CKMoss-Image-RGBA/__init__.py`。

## 放置权重

两份文件在[同一个 HF 仓库](https://huggingface.co/ChenkinLab/CKMoss-Image-RGBA/tree/main)。

| 文件 | 放置位置 | 用途 |
| --- | --- | --- |
| [moss_rgba_vae.safetensors](https://huggingface.co/ChenkinLab/CKMoss-Image-RGBA/resolve/main/vae/moss_rgba_vae.safetensors) | `ComfyUI/models/vae/` | 必需，已合并的 RGBA VAE |
| [moss_rgba_dit_lora.safetensors](https://huggingface.co/ChenkinLab/CKMoss-Image-RGBA/resolve/main/loras/moss_rgba_dit_lora.safetensors) | `ComfyUI/models/loras/` | 可选，MOSS-Image-SFT 配套 LoRA |

本项目提供 VAE 和 LoRA，需要配合 MOSS-Image 基础模型及其文本编码器。

## 开始生成

将工作流 JSON 拖进 ComfyUI：

- [只使用 RGBA VAE](workflows/vae_only.json)：不加载 DiT LoRA。
- [RGBA VAE + DiT LoRA](workflows/with_lora.json)：通过 `Load LoRA (Model Only)` 加载，默认强度 `1.0`。

在 `Load Diffusion Model` 和 `Load CLIP` 中选择已有的 MOSS-Image-SFT 和配套文本编码器；`Load CLIP` 的类型选择 `moss_image`。在 **Load MOSS RGBA VAE** 中选择本项目的 VAE。

输入主体、外观、姿态和风格描述，末尾可加 `transparent background`。示例使用 Euler、30 步、CFG 4；宽高为 16 的倍数。

**VAE Decode → Save Image** 会保留四通道 PNG。需要分别处理颜色和遮罩时，接上 **Split RGBA Image**；其 `mask` 遵循 ComfyUI 的约定：白色透明，黑色不透明。要重新合并，可使用 `Join Image with Alpha`。

示例图片由 RGBA VAE + DiT LoRA 实际生成；展示底色与棋盘格用于呈现透明区域，不写入原始 PNG。

<img src="assets/showcase.png" alt="CKMoss Image RGBA examples" width="100%">

## 致谢

基于 [MOSS-Image](https://github.com/OpenMOSS/MOSS-Image) 和 [FLUX.2 VAE](https://github.com/black-forest-labs/flux2#flux2-autoencoder)。感谢 [niangao2331](https://github.com/niangao2331) 提供部分图像数据。

代码采用 GPLv3，第三方来源与许可见 [NOTICE](NOTICE)。
