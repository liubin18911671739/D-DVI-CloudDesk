# CN-IsardVDI

CN-IsardVDI 是基于 IsardVDI 改造的云桌面平台。项目通过 Docker Compose 组织多个服务，使用 QEMU/KVM 和 libvirt 管理虚拟桌面，并提供浏览器访问、认证、调度、存储、备份和监控能力。

## 主要能力

- 管理虚拟桌面、模板、媒体、用户、用户组、域、资源和预约。
- 支持 SPICE、noVNC、RDP/Guacamole 等桌面访问方式。
- 支持单体部署，也支持独立 Hypervisor、存储、视频代理和监控节点。
- 支持本地认证，并集成 LDAP、SAML 和 Google OAuth 认证配置。
- 提供 WireGuard 用户/Hypervisor 网络、虚拟磁盘存储和 Backupninja 备份。
- 集成 Prometheus、Grafana、Loki、cAdvisor、Node Exporter 和 Go 统计采集。
- 包含中文化前端、Docker 镜像构建以及 ISO/系统集成相关内容。

## 系统架构

| 层次 | 主要服务 | 职责 |
| --- | --- | --- |
| 入口与静态资源 | `portal`、`static` | 对外提供 HTTP/HTTPS，代理 Web、API、静态资源和查看器 |
| 用户界面 | `frontend/`、`webapp/` | Vue 2 前端、Flask Web 应用和 Socket.IO |
| API 与认证 | `api/`、`authentication/` | REST API、用户资源管理和多 Provider 认证 |
| 调度与虚拟化 | `scheduler/`、`engine/`、`hypervisor` | 预约任务、桌面状态编排、libvirt/QEMU 和 GPU/VFIO |
| 连接与网络 | `vpn`、`guac`、`websockify`、`video`、`squid` | WireGuard、Guacamole、WebSocket、视频代理和网络出口 |
| 数据与存储 | `db`、`storage`、`backupninja` | RethinkDB、虚拟磁盘和备份 |
| 监控 | `stats`、Prometheus、Grafana、Loki | 指标、日志和主机/虚拟机状态采集 |

仓库包含三个独立的 Go 模块：根模块、`guac/` 和 `websockify/`。Python 服务的源代码主要位于 `api/`、`engine/`、`scheduler/` 和 `webapp/`。前端源代码位于 `frontend/`；protobuf 源文件位于 `pkg/proto/`。

## 环境要求

- Docker，以及 Docker Compose 1.28 或更高版本。脚本优先使用 `docker compose`，也兼容 `docker-compose`。
- Git submodule 需要可访问并可正常更新。
- 前端开发需要 Node.js、Yarn；当前前端为 Vue 2 工程。
- Go、Python、Buf 仅在直接进行对应模块开发或检查时需要；生产运行主要通过 Docker 完成。

## 快速部署

仓库默认使用根目录的 `cecd.cfg`，配置为 `all-in-one`、`production` 和启用统计服务。部署前应检查域名、密码、证书和所有密钥配置，不要直接使用仓库中的默认值。

```bash
# 生成 .env 和 Docker Compose 文件
./build.sh

# 拉取预构建镜像并启动
docker compose pull
docker compose up -d
```

如果需要本地构建镜像：

```bash
docker compose build
docker compose up -d
```

`build.sh` 会读取所有 `cecd*.cfg`，初始化并更新 submodule，生成 `.env` 和 `docker-compose*.yml`。它在 `build`、`test`、`devel` 用途中还会通过 `docker/codegen/Dockerfile` 执行 protobuf 代码生成。

只生成 Compose、跳过代码生成：

```bash
CODEGEN=false ./build.sh
```

支持的主要 `FLAVOUR`：

```text
all-in-one, hypervisor, hypervisor-standalone, video-standalone,
storage, storage-base, web, webapp, monitor, backupninja
```

支持的 `USAGE`：`production`、`build`、`test`、`devel`。修改配置文件中的 `USAGE` 后再运行 `./build.sh`。脚本会为每个 `cecd*.cfg` 生成对应文件，因此使用临时配置时应避免目录中同时存在不需要的配置文件。

## 开发与验证

### 前端

```bash
cd frontend
yarn
yarn serve
yarn lint --no-fix --max-warnings 0
yarn test
yarn build
yarn test:e2e
```

### Go

三个模块需要分别测试：

```bash
go test ./...
(cd guac && go test ./...)
(cd websockify && go test ./...)
```

### protobuf 与 Python 格式

```bash
buf lint
isort --check .
black --check .
```

GitLab CI 当前会检查 conventional commits、Python 格式、前端 lint 和 protobuf lint，并构建 Compose 文件与 Docker 镜像。根 Go 测试、独立 Go 模块测试和端到端测试目前不在启用的 CI job 中。

## 生成文件约定

- protobuf 生成结果位于 `pkg/gen/`，不要直接修改；修改 `pkg/proto/` 或 `buf*.yaml` 后重新生成。
- `docker-compose*.yml` 和 `.env` 由 `build.sh` 产生。修改服务定义时优先修改 `docker-compose-parts/`、`docker/` 或对应服务源代码。
- 运行构建脚本前后请检查 `git diff`，避免把本地配置、生成结果或密钥意外提交。

## 目录说明

```text
api/                  Flask API
authentication/       Go 认证服务
component/_common/    Python 服务共享代码
docker/               服务 Dockerfile、脚本和基础设施组件
docker-compose-parts/ Compose 服务片段
engine/               虚拟桌面编排与 Hypervisor 管理
frontend/             Vue 2 前端
guac/                 Guacamole Go 服务/库
pkg/proto/             protobuf 定义
scheduler/             预约调度服务
stats/                 统计采集服务
webapp/                Flask Web 应用
websockify/            WebSocket 到 TCP 代理
```

## 外部资源

项目历史上发布过 CN-IsardVDI ISO 和 Docker 镜像资源。外部下载地址、账号和密码可能随版本变化，部署时应以实际配置和发布说明为准，不应将 README 中的示例凭据用于生产环境。
