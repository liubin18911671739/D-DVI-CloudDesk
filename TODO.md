# TODO

以下事项来自当前代码、配置和 CI 的明确缺口，按优先级整理。完成事项时应同步删除对应条目，并补充测试或验证记录。

## 高优先级

- [ ] **移除固定凭据和密钥**：`cecd.cfg`、`cecd.cfg.example`、提交的 Compose 文件和旧 README 中存在默认密码或静态密钥。改为首次部署生成或由外部环境注入，并重新检查历史配置是否已泄露。
- [ ] **收紧网络入口**：`websockify/main.go` 的 `CheckOrigin` 无条件返回 `true`，并根据 URL 中的主机和端口直接建立 TCP 连接。增加可信来源、目标主机白名单和端口范围校验。
- [ ] **限制 API 的跨域来源**：`api/src/api/__init__.py` 将 Socket.IO 的 `cors_allowed_origins` 设置为 `*`。结合 portal 和实际部署域名配置允许来源。
- [ ] **修复 Guacamole 会话列表**：`guac/cmd/guac/guac.go` 构造 `/sessions/` 结果时没有递增索引，多连接时会覆盖第一个元素；补充多连接单元测试。
- [ ] **修复 Guacamole HTTP 响应体生命周期**：`guac/cmd/guac/guac.go` 的认证检查仅在默认分支关闭响应体，成功、未授权和读取错误路径也应保证关闭。

## CI 与构建

- [ ] **统一 CI 配置文件命名**：`.gitlab-ci.yml` 仍创建和使用 `isardvdi*.cfg`，而 `build.sh` 只读取 `cecd*.cfg`；统一为当前命名并验证所有构建 job。
- [ ] **修正 CI Compose 文件引用**：配置文件名会影响 `build.sh` 生成的 Compose 文件名，但 CI 后续使用固定的 `docker-compose.$DOCKER_COMPOSE.yml`；修正配置名或改为引用实际生成文件。
- [ ] **启用 protobuf breaking check**：`.gitlab-ci.yml` 中的 `buf breaking` 仍是注释状态；确定基线仓库或版本后加入 CI。
- [ ] **明确端到端测试策略**：`.gitlab-ci.yml` 中 Selenium/Cypress job 全部被注释，虽然 `frontend/tests.sh` 和前端 E2E 配置仍存在；恢复可运行的 job，或在 CI 文档中明确暂不执行的原因。
- [ ] **统一生成文件策略**：确认 `docker-compose*.yml` 是否应纳入版本控制，并保证提交的 Compose 文件与当前 `cecd.cfg` 一致；不要让过期生成结果代表实际配置。

## 已标记的功能缺口

- [ ] **完成调度器未实现动作**：`scheduler/src/scheduler/lib/scheduler.py` 的多个动作校验路径仍返回 `Action not implemented`，补齐支持的动作或从界面隐藏未支持项。
- [ ] **补充认证错误处理**：`authentication/transport/http/http.go` 多处仍标记 `Better error handling`，统一错误响应格式、日志和对外暴露的信息。
- [ ] **补充认证 Provider 自动注册**：`authentication/authentication/authentication.go` 和 `authentication/authentication/provider/saml.go` 仍保留 Provider 自动注册 TODO。
- [ ] **完善 Hypervisor 选择策略**：`engine/engine/engine/services/lib/qcow.py` 的多个位置仍标记需要按负载、权重或随机策略改进 Hypervisor 选择。
- [ ] **增加 libvirt 操作超时**：`stats/cmd/stats/main.go` 明确标记缺少 libvirt timeout，避免采集阻塞统计服务。
- [ ] **完善预约页面刷新**：`frontend/src/store/modules/planning.js` 的 `changePlanningCurrentView` 在选择 profile 后尚未重新获取事件。
- [ ] **处理 RDP 不稳定状态**：`frontend/src/views/Rdp.vue` 对 Guacamole `UNSTABLE` 状态仍只有 TODO，应定义重试、提示或断开策略。

## 测试覆盖

- [ ] **补充 websockify 和 stats 测试**：当前未发现对应的 Go `*_test.go` 文件，至少覆盖连接校验、代理错误和采集超时场景。
- [ ] **把独立 Go 模块测试纳入 CI**：根模块、`guac/` 和 `websockify/` 需要分别执行 `go test ./...`，当前 CI 未覆盖这些命令。
- [ ] **明确 Python 测试入口**：API、Engine、Scheduler 和 Webapp 的测试形态不统一；整理可执行命令、依赖服务和测试数据，避免只依赖 Docker 镜像构建验证。
