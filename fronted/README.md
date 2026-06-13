# 前端 (fronted)

Vue3 博客前端 — 管理后台 + 公开站点 + ByteMD。

## 启动

```bash
npm run install:all
npm run dev:admin    # 管理后台 http://localhost:5174
npm run dev:web      # 前台 http://localhost:5173
```

需先启动 `../backend`。

## 目录

```
fronted/
├── admin/         # 管理后台（ByteMD 编辑器）
├── web/           # 公开前台
├── public/        # 原静态镜像（参考）
├── scripts/       # 静态站镜像工具（可选）
└── package.json
```

默认账号：`admin` / `admin123`
