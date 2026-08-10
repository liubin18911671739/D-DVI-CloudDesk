# Repository Instructions

## Structure

- This is a Docker Compose multi-service repository. `api/`, `engine/`, `authentication/`, `scheduler/`, `webapp/`, `frontend/`, `guac/`, and `websockify/` are separate service boundaries; service images and Compose fragments live under `docker/` and `docker-compose-parts/`.
- The root Go module covers shared/root Go code. `guac/` and `websockify/` are independent Go modules and must be tested separately.
- Protobuf sources are under `pkg/proto`; generated output is under ignored `pkg/gen`.

## Build And Run

- `./build.sh` requires Docker and Docker Compose >= 1.28. It reads every `cecd*.cfg`, updates submodules, writes `.env` and `docker-compose*.yml`, and runs code generation for build/test/devel usages. Inspect generated-file changes before committing.
- Use `CODEGEN=false ./build.sh` when Compose generation is needed without code generation. The default tracked `cecd.cfg` selects `FLAVOUR=all-in-one` and `USAGE=production`; set `USAGE=build`, `test`, or `devel` in the config when those generated Compose variants are required.
- After generation, run `docker compose pull && docker compose up -d` for published images, or `docker compose build && docker compose up -d` to build locally. `build.sh` also supports the legacy `docker-compose` command.
- Do not edit generated `pkg/gen` or generated Compose files directly; change `pkg/proto`, `buf*.yaml`, `docker-compose-parts/`, or the source service files instead.

## Verification

- Frontend: from `frontend/`, run `yarn`, then `yarn lint --no-fix --max-warnings 0`; focused commands are `yarn test`, `yarn build`, and `yarn test:e2e`.
- Go: run `go test ./...` separately from the repository root, `guac/`, and `websockify/`.
- Protobuf: run `buf lint` from the repository root. Code generation is containerized by `./build.sh` and uses the pinned toolchain in `docker/codegen/Dockerfile`.
- Python formatting checks match CI: from the repository root, run `isort --check .` followed by `black --check .`.
- The GitLab CI lint jobs also enforce conventional commit messages and frontend linting with zero warnings; no repository-wide Python or end-to-end test command is enabled there.
