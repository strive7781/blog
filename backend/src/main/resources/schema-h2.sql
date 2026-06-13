CREATE TABLE IF NOT EXISTS admin_user (
    id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    username    VARCHAR(50)  NOT NULL UNIQUE,
    password    VARCHAR(255) NOT NULL,
    nickname    VARCHAR(100),
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS category (
    id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    slug        VARCHAR(100) NOT NULL UNIQUE,
    description VARCHAR(500),
    sort_order  INT DEFAULT 0,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tag (
    id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    slug        VARCHAR(100) NOT NULL UNIQUE,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS article (
    id           BIGINT AUTO_INCREMENT PRIMARY KEY,
    title        VARCHAR(200) NOT NULL,
    slug         VARCHAR(200) NOT NULL UNIQUE,
    summary      CLOB,
    content_md   CLOB NOT NULL,
    cover_url    VARCHAR(500),
    category_id  BIGINT,
    status       INT DEFAULT 0,
    view_count   INT DEFAULT 0,
    published_at TIMESTAMP,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS article_tag (
    article_id BIGINT NOT NULL,
    tag_id     BIGINT NOT NULL,
    PRIMARY KEY (article_id, tag_id)
);

CREATE TABLE IF NOT EXISTS media (
    id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    filename    VARCHAR(255) NOT NULL,
    url         VARCHAR(500) NOT NULL,
    mime_type   VARCHAR(100),
    size_bytes  BIGINT,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS site_config (
    id           BIGINT AUTO_INCREMENT PRIMARY KEY,
    config_key   VARCHAR(100) NOT NULL UNIQUE,
    config_value CLOB,
    description  VARCHAR(255)
);

MERGE INTO site_config (config_key, config_value, description) KEY(config_key) VALUES
('site_title', 'Kyle''s Blog', '站点标题'),
('site_subtitle', '记录学习与生活的点滴', '站点副标题'),
('site_description', '个人技术博客', '站点描述'),
('avatar_url', 'https://s2.loli.net/2025/02/23/AMkCrfzyFsBQE3D.png', '头像'),
('background_url', 'https://cdn.staticaly.com/gh/L-Carry/pic_bed@main/img/day01.jpg', '背景图'),
('theme_color', 'rgb(57, 197, 187)', '主题色'),
('footer_text', '©2021-2026 By Kyle Violet', '页脚文字'),
('notice_html', '欢迎使用博客管理系统', '公告栏');

MERGE INTO category (name, slug, description, sort_order) KEY(slug) VALUES
('学习笔记', 'study', '技术学习记录', 1),
('随写', 'essay', '随笔杂谈', 2);

MERGE INTO tag (name, slug) KEY(slug) VALUES
('Java', 'java'),
('Spring Boot', 'spring-boot'),
('Vue', 'vue');
