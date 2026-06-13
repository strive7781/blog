CREATE DATABASE IF NOT EXISTS blog DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE blog;

CREATE TABLE IF NOT EXISTS admin_user (
    id          BIGINT PRIMARY KEY AUTO_INCREMENT,
    username    VARCHAR(50)  NOT NULL UNIQUE,
    password    VARCHAR(255) NOT NULL,
    nickname    VARCHAR(100),
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS category (
    id          BIGINT PRIMARY KEY AUTO_INCREMENT,
    name        VARCHAR(100) NOT NULL,
    slug        VARCHAR(100) NOT NULL UNIQUE,
    description VARCHAR(500),
    sort_order  INT DEFAULT 0,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tag (
    id          BIGINT PRIMARY KEY AUTO_INCREMENT,
    name        VARCHAR(100) NOT NULL,
    slug        VARCHAR(100) NOT NULL UNIQUE,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS article (
    id           BIGINT PRIMARY KEY AUTO_INCREMENT,
    title        VARCHAR(200) NOT NULL,
    slug         VARCHAR(200) NOT NULL UNIQUE,
    summary      TEXT,
    content_md   LONGTEXT     NOT NULL,
    cover_url    VARCHAR(500),
    category_id  BIGINT,
    status       TINYINT DEFAULT 0 COMMENT '0=draft 1=published',
    view_count   INT DEFAULT 0,
    published_at DATETIME,
    created_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at   DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_article_status (status),
    INDEX idx_article_published (published_at)
);

CREATE TABLE IF NOT EXISTS article_tag (
    article_id BIGINT NOT NULL,
    tag_id     BIGINT NOT NULL,
    PRIMARY KEY (article_id, tag_id)
);

CREATE TABLE IF NOT EXISTS media (
    id          BIGINT PRIMARY KEY AUTO_INCREMENT,
    filename    VARCHAR(255) NOT NULL,
    url         VARCHAR(500) NOT NULL,
    mime_type   VARCHAR(100),
    size_bytes  BIGINT,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS site_config (
    id           BIGINT PRIMARY KEY AUTO_INCREMENT,
    config_key   VARCHAR(100) NOT NULL UNIQUE,
    config_value TEXT,
    description  VARCHAR(255)
);

-- admin / admin123  BCrypt
INSERT INTO admin_user (username, password, nickname) VALUES
('admin', '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iKTVKIUi', '管理员')
ON DUPLICATE KEY UPDATE username = username;

INSERT INTO site_config (config_key, config_value, description) VALUES
('site_title', 'Kyle''s Blog', '站点标题'),
('site_subtitle', '记录学习与生活的点滴', '站点副标题'),
('site_description', '个人技术博客', '站点描述'),
('avatar_url', 'https://s2.loli.net/2025/02/23/AMkCrfzyFsBQE3D.png', '头像'),
('background_url', 'https://cdn.staticaly.com/gh/L-Carry/pic_bed@main/img/day01.jpg', '背景图'),
('theme_color', 'rgb(57, 197, 187)', '主题色'),
('footer_text', '©2021-2026 By Kyle Violet', '页脚文字'),
('notice_html', '欢迎使用博客管理系统', '公告栏')
ON DUPLICATE KEY UPDATE config_key = config_key;

INSERT INTO category (name, slug, description, sort_order) VALUES
('学习笔记', 'study', '技术学习记录', 1),
('随写', 'essay', '随笔杂谈', 2)
ON DUPLICATE KEY UPDATE slug = slug;

INSERT INTO tag (name, slug) VALUES
('Java', 'java'),
('Spring Boot', 'spring-boot'),
('Vue', 'vue')
ON DUPLICATE KEY UPDATE slug = slug;
