# 后端 (backend)

Spring Boot REST API — 文章、分类、标签、媒体、站点配置。

## 启动

```bash
# MySQL
docker compose up -d
mvn spring-boot:run

# H2 内存库（无需 MySQL）
mvn spring-boot:run "-Dspring-boot.run.profiles=h2"
```

- 端口：`8080`
- 默认账号：`admin` / `admin123`

## 目录

```
backend/
├── src/                 # 源码
├── docker-compose.yml   # MySQL
└── pom.xml
```
