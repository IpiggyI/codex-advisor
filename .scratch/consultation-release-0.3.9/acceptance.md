# 0.3.9 发布与双端安装验收

日期：2026-11-17。用户授权：发布，然后安装到 WSL 和 Windows 两侧。

## 发布范围

版本为 `0.3.9`，沿用 GitHub 市场源码发布方式。包含具名独立函数结果兼容、
第三次累计失败停用、脱敏原生执行诊断，以及此前本地提交 `97e16ba` 的多会话文件选择。
对应排查记录位于 `../consultation-named-output/issues/` 和 `../consultation-timeout/issues/`。
本版补齐 README、清单及 `docs/releases/0.3.9.html`，旧版手册保持冻结。

主会话执行全部外部操作，不停止用户进程，不编辑托管缓存，不修改失败计数或钩子信任。
本线程累计失败已达三，咨询不可用；不再调用过程咨询，包括完成前咨询。
安装验证只检查新进程启动、已安装文件和入口，不增加真实模型请求。

## 前置检查

- WSL 和 Windows 的 Codex CLI 均为 `0.169.0`。两侧市场均指向 GitHub 仓库 `IpiggyI/codex-advisor`。
- Windows 原生目标为 `C:\Users\Shy\.codex`，命令行显式设置该目录。
- Windows 源码检查已通过：原生执行 37 项、本地端点请求 10 项、失败存储 9 项。
- 宿主模式差异检查覆盖 18 类，缺失类型为零。
- 全量语料扫描 843 份记录，回放 31476 个位置：31381 个通过，95 个回滚位置按设计拒绝，普通失败为零；8697 个位置跳过，保持未验证。
- 原生语料链 11 项通过，覆盖实际存在的 11 类历史项，使用顾问目录实际启用的 Responses Lite 模式；没有顾问使用的非 Lite 模式没有强行覆盖。
- 最终 `sh tests/verify.sh` 退出零，8 项 Windows 专属测试在 WSL 跳过；镜像 41 项、措辞 66 项、版本手册 3 项通过，差异空白检查通过。
- HTML 解析、唯一标识、内部锚点及本地链接检查通过；页面视觉未重新验收。

所有检查证据保存在本目录的 `evidence/`。新版本没有改变钩子定义，现有用户钩子信任
与既有会话重载分别保持未验证；新安装不能证明这两个边界。

## 发布与安装

源码已经具备发布条件；提交与远端引用、两侧标准安装与重装、配套入口检查以及新进程启动待回填。

## 保留的无关工作

`.scratch/consultation-empty-tools/acceptance.md` 的既有改动，`.agent-discuss/`、
`.fable-advisor/`、`.scratch/consultation-stale-cell/`、旧 Windows 重装 JSON 和两个
`.scratch/consultation-native-error/audit-native-*.patch` 均不纳入本次提交。
