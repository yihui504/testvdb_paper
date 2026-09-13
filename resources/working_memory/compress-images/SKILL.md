---
name: compress-images
description: 压缩项目图片以减体积/加快编译（高 DPI 降采样、PNG 无损压缩、JPEG 重存、BMP/TIFF 转 PNG，原图备份 .xept_uncompressed）。经 pwsh 调 scripts/compress_images.py。
---

# Compress Images（压缩图片）

减小项目体积、加快编译。

## 工作流
```
1. 扫描 — 列出所有图片及大小（`pwsh` ls 或 `glob`）
2. 分析 tex — 找哪些图片被 \includegraphics 引用
3. 汇报 — 展示引用/未引用图片列表
4. 未引用图片 — 改名加 xept_unused 标记（自动跳过编译）
5. 引用的大图片 — 经 `pwsh` 调 scripts/compress_images.py 压缩
6. 验证 — 报告压缩前后对比
```

## Step 1: 扫描与分析
1. `pwsh` 跑 ls（或 `glob`）列出所有文件
2. `grep` `.tex` 文件搜 `\includegraphics` 引用
3. 交叉对比：哪些图被引、哪些没被引
4. 汇报用户

## Step 2: 处理未引用文件
未被任何 `.tex` 引用的图仍会被打包进编译。用 `pwsh` 跑 mv 加 `xept_unused` 标记：
`figures/old_draft.png` → `figures/old_draft.xept_unused.png`
编译时自动跳过。用户在文件树能看到，需要时改名恢复。

## Step 3: 压缩引用的大图片
经 `pwsh` 调本插件脚本 `scripts/compress_images.py`：
```bash
python scripts/compress_images.py                          # 所有 >500KB 图片
python scripts/compress_images.py --min-size-kb 1000        # 只压 >1MB
python scripts/compress_images.py --paths figures/big.png   # 指定文件
python scripts/compress_images.py --quality 80 --max-dpi 600
```
脚本自动：
- 高 DPI 图降到 600 DPI（最有效的压缩手段）
- PNG 无损最大压缩
- JPEG quality 85 重存
- BMP/TIFF 转 PNG
- 原图保留为 `filename.xept_uncompressed.<ext>`（编译时自动跳过）
- 压缩效果 <5% 的自动跳过恢复

## Step 4: 验证
1. 报告压缩结果与节省空间
2. 检查是否降到 30MB 免费阈值以下
3. 仍超则建议进一步操作（降 JPEG quality、删不需要的文件）

## 重要规则
- **经 `pwsh` 调 `scripts/compress_images.py`** 压图（替代原平台 compress_images MCP 工具）
- **原图安全**：`.xept_uncompressed` 文件用户可见，编译跳过
- **恢复**：把 `file.xept_uncompressed.png` 改回原名即可恢复
- **LaTeX 兼容**：压缩后文件名不变，`\includegraphics` 引用不受影响
- **BMP/TIFF 转换**：转 PNG 后扩展名变了，可能需更新 tex 引用