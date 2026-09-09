---
name: production-project-iteration
description: "用于可能进入 PR、CI、GitOps 和生产验收链路的非琐碎项目变更，按需求定界、受限委派、独立验证、受控部署和线上验收完成闭环。"
---

# Production Project Iteration

当非琐碎变更可能进入 PR、CI、GitOps 和生产环境时使用本流程。它把工作组织为需求定界、受限实现、独立验证、受控部署和生产验收五个连续关口。

## 核心原则

1. 先判断主线是否已经具备目标能力，再决定实现还是验证。
2. 委派实现不等于委派判断。编排者必须用真实 diff、测试和仓库规则独立验收。
3. coding agent 只获得代码工作范围。Forge API、push、创建或合并 PR、Argo sync、`kubectl`、SSH 和生产 smoke test 都属于 live ops，必须由获授权的人显式执行。
4. 镜像构建或推送成功不是完成。完成要求代码主线、Forge、GitOps pin 和实际工作负载的 SHA 收敛，并且线上健康检查和真实客户端路径可用。
5. 每一阶段都产出可审计证据，并明确下一阶段的输入、责任人和停止条件。

## 1. 建立干净基线并判定已有能力

1. 获取远端最新状态，在独立 clean worktree 或确认无未提交改动的工作区中检出 `origin/main`。不要覆盖或清理用户现有修改。
2. 记录基线 SHA，并核对权威代码托管端的主线 SHA。若多个 Forge 或镜像仓库参与交付，明确各自角色和同步方向。
3. 从实现、测试、ADR、配置和运行路径检查目标能力，不要只按文件名或 issue 状态判断。
4. 在 clean `origin/main` 上运行最小但足以证明能力的目标测试。
5. 按结果分流：
   - 已具备且测试通过：转为验证或配置任务，不创建重复实现。
   - 部分具备：只补缺失的验收标准。
   - 不具备：进入实现。
   - 证据冲突或基线不一致：停止，先解决基线和需求歧义。

## 2. 编写 task packet

在委派前创建可引用的 task packet，至少包含：

- `Goal`：可观察的目标结果。
- `Non-goals`：本轮明确不做什么。
- `Acceptance Criteria`：可逐项验证的行为、错误路径和兼容性要求。
- `Scope`：允许修改的仓库、目录和接口。
- `Constraints`：架构、依赖、安全、迁移、兼容和操作限制。
- `Verification`：必须执行的测试、静态检查、仓库 guard 和运行验证。
- `Handoff`：预期 diff、已知风险、待人工操作及证据格式。

把 packet 保存为稳定路径或标识。任何范围变化都先更新 packet，再继续实现。

## 3. 受限委派实现

1. 向 coding agent 提供 task packet、clean 基线 SHA、允许修改的范围和禁止事项。
2. 明确禁止 agent 执行 live ops，包括 Forge API、push、PR 操作、`kubectl`、SSH、Argo sync 和生产环境调用。
3. 要求 agent 返回：修改摘要、实际变更文件、测试命令与结果、未解决事项和风险。
4. 不采信 agent 的完成声明。将其输出视为待验证的实现候选。
5. 对仅修改 1 到 2 行的机械式 SHA re-pin 或版本更新，可以跳过完整委派环，但仍必须执行 diff 检查、相关 guard 和后续收敛验证。

## 4. 编排者独立验证

按以下顺序检查：

1. 查看真实 `git status`、`git diff --stat` 和完整 diff，确认没有越界文件、生成垃圾、意外依赖或隐蔽配置变化。
2. 执行 task packet 指定的目标测试，再运行由 diff 触发的相关测试集。
3. 执行仓库 guard，包括 lint、格式、类型检查、secret 扫描、依赖或策略检查。
4. 对错误路径、兼容性和配置默认值做针对性验证。
5. 让 coding agent 或独立 reviewer 以只读模式审查最终 diff。reviewer 不得修改代码或执行 live ops。
6. 将每条 AC 标为通过、失败或未验证。存在失败或关键项未验证时不得进入 PR。

## 5. PR 与 CI 关口

1. 由获授权的人提交、push 并创建 PR。提交信息必须绑定 task packet 的稳定标识或路径。
2. PR 描述包含 Goal、Non-goals、AC、验证证据、风险和回滚方式。
3. CI 根据 diff 映射测试集，不能只运行固定的最小 smoke test。跨层变更必须覆盖相应层级。
4. CI PR gate 至少包含确定性检查、目标测试、必要的集成测试和一次只读 diff review。
5. 仅在 required checks 全部通过、review 已处理、真实 head SHA 明确后合并。
6. 合并后重新记录主线 SHA。不要假定 PR head、merge commit 和构建产物 SHA 相同。

## 6. GitOps 更新与受控部署

1. 等待 CI 为目标主线 SHA 构建并发布不可变产物。验证产物标签或 digest 确实对应该 SHA。
2. 在权威 GitOps 仓库中只更新目标环境的 pin 或配置，通过独立 PR 审查和合并。
3. GitOps PR gate 必须校验应用 SHA、产物 SHA 和声明式配置 pin 的对应关系。不收敛时阻断合并。
4. Argo 和集群操作保持人工显式执行并留证。若环境使用自动同步，也要由人确认目标 Application、revision 和同步结果。
5. 需要手动同步时，先刷新 root 状态，只同步目标子 Application 或受限资源，再同步 child。禁止无边界同步整个 root。
6. 等待 Application 达到 `Synced` 和 `Healthy`，随后验证 Deployment rollout 完成、预期镜像或 digest 已生效、期望副本全部 Ready。

## 7. 生产验收

按由浅入深的顺序执行并保存输出：

1. Deployment rollout 状态。
2. 工作负载实际镜像标签或 digest。
3. 服务 `/healthz` 或等价健康端点。
4. 一条真实远端 CLI 或客户端路径，覆盖认证、网络、路由和 API，而不是只从 Pod 内部访问。
5. 关键功能的最小生产 smoke test，避免破坏性写入。

最终建立收敛表，至少列出：

- 应用仓库主线 SHA。
- 权威 Forge 主线 SHA。
- CI 构建所用 SHA 和产物 digest。
- GitOps 仓库 revision 及其配置 pin。
- Argo observed revision。
- Deployment 实际镜像或 digest。
- 健康检查和真实客户端验证结果。

只有这些证据一致且线上 API 可用，任务才算完成。任一 SHA 不一致、状态不健康或真实客户端失败时，停止宣布完成，定位是代码同步、构建、GitOps、rollout、认证还是服务路径问题。

## 自动化边界

按成本和权限分层，不把生产操作塞进本地 hook：

- `pre-commit`：只做快速、确定性的 lint、格式检查和 secret 扫描。
- `commit-msg`：强制提交绑定 task packet 标识。
- CI PR gate：执行 diff 到测试集映射、仓库 guard 和 coding agent 只读 review。
- GitOps PR gate：校验应用 SHA、产物和环境 pin 收敛。
- 人工显式步骤：Argo sync、`kubectl`、SSH、生产 smoke test、push、PR 创建与合并。

## 失败与回滚

- CI 失败：保留失败日志和对应 SHA，修复代码，不绕过 required gate。
- GitOps 不收敛：停止同步，核对主线、产物和 pin，不用重新推同名可变标签掩盖问题。
- rollout 或健康检查失败：保留 Argo、Deployment、事件和日志证据，按既定 GitOps 回滚方式恢复已知良好 pin。
- 真实客户端失败但健康检查成功：优先检查认证、路由、环境配置和 API 兼容性，不把 `/healthz` 成功当作服务可用。

每次失败修复后，从最早受影响的关口重新验证，不只重跑最后一步。
