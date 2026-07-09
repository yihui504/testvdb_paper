<!-- Generated: 2026-05-24 | Updated: 2026-05-24 -->

# mftui

## Purpose
工作空间根目录，包含 TestVDB 向量数据库质量保障工具项目及辅助配置文件。

## Key Files
| File | Description |
|------|-------------|
| `deepseekapikey.txt` | DeepSeek LLM API 密钥文件 |
| `shrink_docker.txt` | Docker 清理相关笔记 |
| `开题报告.txt` | 项目开题报告 |

## Subdirectories
| Directory | Purpose |
|-----------|---------|
| `TestVDB/` | 向量数据库自动化缺陷挖掘工具（Rust 项目，详见 `TestVDB/AGENTS.md`） |
| `.trae/` | Trae IDE 规则配置（项目级编码规范） |
| `.deepseek/` | DeepSeek 模型指令配置 |

## For AI Agents

### Working In This Directory
- 本工作空间的核心项目是 `TestVDB/`，所有代码修改应在该目录下进行
- API 密钥位于 `deepseekapikey.txt`，运行时需设置 `DEEPSEEK_API_KEY` 环境变量
- 遵循 `.trae/rules/` 中的编码规范（Karpathy 风格：简洁优先、外科手术式修改、目标驱动）

### Testing Requirements
- TestVDB 使用 `cargo test` 运行单元测试
- 集成测试依赖 Docker 环境

### Common Patterns
- Rust 2024 edition
- 异步编程使用 tokio 运行时
- LLM 集成通过 DeepSeek API

## Dependencies

### External
- Rust toolchain (edition 2024)
- Docker（用于沙箱环境）
- DeepSeek API（LLM 编排）
