**案例用途**

以下案例来自 2026-09-19 的跨项目复盘。只用于解释容易误判的边界；仓库版本、CI、政策或运行状态需要按任务重新核对。无 nmem 时，下文已包含理解方法所需的事实，不要求为了使用 skill 先配置外部服务。

**缺凭证 skip 隐藏错误调用**

Coding-Agent-Loop 的真实 provider 测试曾向 `create_agent` 传入不存在的 `provider_name` 参数。无凭证时提前 skip，运行时没有执行到错误调用；diagnostics 揭示了问题。

可迁移做法：默认路径可以允许可选测试 skip，但对准备支持的真实路径仍需验证接口契约。只看到“没有 failed”不能证明该路径可执行。

来源：[原始线程](nowledgemem://thread/opencode-ses_276395de2ffeg8z0sczqvyhylr)，message index 134。

**改断言可以保持原验收目标**

最长链测试曾要求 child 精确输出特定字符串。原 ADR 允许 provider variance；后来改为验证一次 subagent 调用、hidden child 消息、tool result 与实际 child 输出一致，以及后续持久化、extract 和 metric 调用。用户复核认可该修改仍在证明链路契约。

有凭证环境记录三项通过，用户另一环境却是一项通过、两项因缺凭证跳过，两者不冲突。当前复盘所读最长链还只检查 metric 分数在合法范围，未证明质量门槛。

可迁移做法：对照原契约判断断言调整；将链路执行、模型指令遵循和质量阈值视为不同目标。成功声明绑定实际环境。

来源：同一线程 message index 281–289。不能只读早期 skip 或后期提交标题来推断最终执行结果。

**存储往返不等于完整恢复**

storage-backed 测试读取到的 backing file 是 delta，需要与基底 user message 组合才能重建目标 turn。这能支持 delta 持久化及组合读取，不能证明文件自足或重启后无需进程内状态即可恢复。

可迁移做法：先确认数据所有权与持久化边界；只有目标涉及恢复保证时，再要求相应新进程或重建验证。不要为了“更像 e2e”给无关改动增加恢复演练。

来源：同一线程 message index 128–133；复盘归纳 [nmem learning](nowledgemem://memory/e2e-pr-review-retrospective-20260919)。

**交付配置与 release 生命周期是不同边界**

llm-d-router #2832 让 e2e 消费 standalone Helm chart，经过渲染、Kubernetes 创建、就绪、路由、故障后转发恢复和清理。维护者还要求 helper 从测试包迁到专门的 util 包，以明确公开接口。

其 `helm template + apply` 验证不覆盖 Helm release 的 install/upgrade/rollback。existing-context 的三项聚焦测试通过时，另外 26 项是被筛选排除，并未在该模式下执行。

可迁移做法：用真实交付物减少配置漂移，审查测试生命周期本身；对聚焦结果保留分母和筛选条件。

来源：[PR #2832](https://github.com/llm-d/llm-d-router/pull/2832)、[历史实现与验证记录](nowledgemem://memory/313df22f-0892-4702-bfb1-bc046245e0b7)。

**检查名称相同，检查条件可能不同**

同项目本地带 `--new` 的 lint 曾漏掉全量 CI 检出的未使用返回值。本地 DCO 脚本只检查 trailer 存在，也漏掉了 sign-off 与 commit author 不匹配。

可迁移做法：检查实际命令、配置、基线和判据。不能把“某项检查通过”改写成另一个覆盖更大的检查通过；lint finding 的存在本身也不证明产品运行故障。

来源：上述历史实现与验证记录中的 CI 纠正部分。

**P2 分级与项目合并政策有不同作用**

历史通用角色策略允许 P2 在范围小、无新增风险等条件下择机修复。Coding-Agent-Loop 后来的项目规则则要求本 diff 引入或能够解决的 P2 在合并前修复，除非人在 PR 明确延期。

可迁移做法：查当前任务适用规则，不将任一历史政策升级成普遍原则；也不要为收口随意降低缺陷级别。

来源：[通用策略](nowledgemem://memory/5aa683e8-748a-40c0-b4f1-91a80d0e4a4c)、[项目规则记录](nowledgemem://memory/47708777-c453-494f-a74c-9a887b79fe59)。

**多次 review clean 不补足运行时证据**

PR #648 的两轮 fresh review 对指定 GitOps diff 未发现 P1/P2，但 memory 索引、实际落盘、跨 session 召回来源仍需要业务运行验证。这是当时记录的缺口，不能据此断言今天仍未完成。

本次复盘中，反例 agent 还把“改断言”一概视为降低验收标准，并将“P2 不阻塞”跨项目推广。主持人提供原始用户复核与项目规则后，它撤回过强判断。

可迁移做法：独立会话有助于发现遗漏，判断仍须回到原证据。静态审查、实际运行与业务质量各有证明范围；历史中间状态与最终状态也应分开。

来源：[PR #648 历史边界](nowledgemem://memory/187b3f97-c604-46dc-99e2-fc7b2caad685)、[本次复盘归纳](nowledgemem://memory/e2e-pr-review-retrospective-20260919)。
