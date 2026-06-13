# DESIGN.md

> 复刻 Kyle's Blog — 日系动漫风 Hexo Butterfly 个人博客，全屏壁纸 + 毛玻璃卡片 + Live2D 看板娘。

## 1. Visual Theme & Atmosphere

**Style**: Hexo Butterfly 魔改 · 动漫生活感博客  
**Keywords**: 全屏背景、毛玻璃、青绿主题、卡片瀑布、Live2D、侧边栏、打字机标题、粒子/Canvas  
**Tone**: 温暖、个人化、二次元友好 — NOT 企业 SaaS、NOT 极简黑白  
**Feel**: 像走在夏日日本街头的博客窗口，内容浮在透明卡片上，背景随日/夜切换。

**Interaction Tier**: L2 流畅交互  
**Dependencies**: CSS + jQuery + WOW.js + Typed.js + LazyLoad + Live2D Widget + 多 CDN 插件

## 2. Color Palette & Roles

```css
:root {
  /* Backgrounds */
  --global-bg: #fff;
  --card-bg: #fff;
  --sidebar-bg: #f6f8fa;
  --search-bg: #f6f8fa;
  --surface: rgba(253, 253, 253, 0.95);
  --surface-dark: rgba(25, 25, 25, 0.95);

  /* Text */
  --font-color: #4c4948;
  --text-highlight-color: #1f2d3d;
  --blockquote-color: #6a737d;
  --headline-presudo: #a0a0a0;
  --toc-link-color: #666261;

  /* Accent — 默认主题色 green */
  --theme-color: rgb(57, 197, 187);
  --btn-hover-color: #ff7242;
  --pseudo-hover: #ff7242;
  --text-bg-hover: rgba(143, 188, 143, 0.7);

  /* Borders & dividers */
  --hr-border: #c7dec7;
  --hr-before-color: #b1d0b1;
  --tab-border-color: #f0f0f0;
  --border-color: #c9c9c9;
  --border-style: 1px solid rgba(169, 169, 169, 0.7);

  /* Code blocks */
  --hl-bg: #282c34;
  --hl-color: #eff;
  --hltools-bg: #1c1c1c;

  /* Glassmorphism */
  --trans-light: rgba(253, 253, 253, 95%);
  --trans-dark: rgba(25, 25, 25, 95%);
  --blur-num: blur(20px) saturate(120%);
  --backdrop-filter: var(--blur-num);

  /* Background images */
  --default-bg: url(https://cdn.staticaly.com/gh/L-Carry/pic_bed@main/img/day01.jpg);
  --darkmode-bg: url(https://cdn.staticaly.com/gh/L-Carry/pic_bed@main/img/night01.jpg);

  /* RGB variants */
  --theme-color-rgb: 57, 197, 187;
  --font-color-rgb: 76, 73, 72;
  --card-shadow-rgb: 7, 17, 27;

  /* Semantic palette (主题切换) */
  --color-red: rgb(241, 71, 71);
  --color-orange: rgb(241, 162, 71);
  --color-yellow: rgb(241, 238, 71);
  --color-purple: rgb(179, 71, 241);
  --color-blue: rgb(102, 204, 255);
  --color-green: rgb(57, 197, 187);
  --color-pink: rgb(237, 112, 155);
  --color-heoblue: rgb(66, 90, 239);

  /* Elevation */
  --card-box-shadow: 0 3px 8px 6px rgba(7, 17, 27, 0.05);
  --card-hover-box-shadow: 0 3px 8px 6px rgba(7, 17, 27, 0.09);
}
```

**Color Rules:**
- 所有强调交互使用 `--theme-color`，默认青绿色
- 卡片/导航/侧边栏使用 `--trans-light` + `backdrop-filter`
- 禁止在组件内硬编码 hex，沿用 Butterfly 变量体系

## 3. Typography Rules

**Font Stack:**
```css
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&display=swap');

body {
  font-family: 'LXGW WenKai', 'Noto Sans SC', 'Microsoft YaHei', sans-serif;
  font-size: 15.5px;
  line-height: 1.7;
  letter-spacing: 0.02em;
  color: var(--font-color);
}
@font-face {
  font-family: 'YSHST';
  src: url(/font/优设好身体.woff2);
}
```

| Role | Font | Size | Weight | Line Height | Letter Spacing |
|------|------|------|--------|-------------|----------------|
| Hero H1 (#site-title) | LXGW / Noto Sans SC | 46.5px | 700 | 1.2 | 0.02em |
| Hero Subtitle | 同上 | 18px | 400 | 1.6 | 0.02em |
| Nav | 同上 | 15.5px | 500 | 1.5 | 0 |
| Article Title | 同上 | 20.15px | 700 | 1.4 | 0 |
| Body | 同上 | 15.5px | 400 | 1.7 | 0.02em |
| Meta/Label | 同上 | 12px | 400 | 1.5 | 0 |
| Code | Consolas, monospace | 14px | 400 | 1.6 | 0 |

**Typography Rules:**
- 中文正文 ≥ 15.5px，长文阅读舒适
- 标题 hover 变 `--theme-color`
- **NEVER use**: 仅英文字体栈导致中文回退宋体

**Text Decoration:**
- Hero h1: 白色投影（全屏背景上），无渐变
- Section 标题: 左侧竖线伪元素 + `--headline-presudo`

## 4. Component Stylings

### Buttons
```css
.btn, .button--animated {
  background: var(--theme-color);
  color: var(--btn-color, #fff);
  border: none;
  border-radius: 6px;
  padding: 0.4rem 1rem;
  transition: all 0.3s ease;
  cursor: pointer;
}
.btn:hover, .button--animated:hover {
  background: var(--btn-hover-color);
  transform: translateY(-1px);
}
.btn:active { transform: translateY(0); }
.btn:focus-visible { outline: 2px solid var(--theme-color); outline-offset: 2px; }
.btn:disabled { opacity: 0.5; pointer-events: none; }
```

### Cards (recent-post-item / card-widget)
```css
.recent-post-item, .card-widget {
  background: var(--trans-light);
  backdrop-filter: var(--backdrop-filter);
  border-radius: 12px;
  box-shadow: var(--card-box-shadow);
  transition: box-shadow 0.3s, transform 0.3s;
}
.recent-post-item:hover, .card-widget:hover {
  box-shadow: var(--card-hover-box-shadow);
}
.recent-post-item:focus-within {
  outline: 2px solid rgba(var(--theme-color-rgb), 0.4);
}
```

### Navigation (#nav)
```css
#nav {
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 100;
  transition: background 0.3s, backdrop-filter 0.3s;
}
#nav .site-page:hover { color: var(--theme-color); }
#nav .site-page:focus-visible { outline: 2px solid var(--theme-color); }
#nav.show {
  background: var(--trans-light);
  backdrop-filter: var(--backdrop-filter);
}
```

### Links
```css
a { color: var(--theme-color); text-decoration: none; transition: color 0.2s; }
a:hover { color: var(--pseudo-hover); }
a:focus-visible { outline: 2px dashed var(--theme-color); }
```

### Tags
```css
.article-meta__tags a, .card-tag-cloud a {
  padding: 2px 8px;
  border-radius: 6px;
  background: rgba(var(--theme-color-rgb), 0.12);
  font-size: 12px;
}
.article-meta__tags a:hover {
  background: var(--text-bg-hover);
}
```

## 5. Layout Principles

- **结构**: `#page-header.full_page` Hero → `#content-inner.layout` 主内容（左文章 + 右 sidebar）→ `#footer`
- **容器**: 主内容 max-width ~1400px，文章区 + 300px 侧边栏
- **间距**: 卡片 gap 16–20px；section 上下 24px+
- **Hero**: 100vh 全屏，`#web_bg` 固定背景图
- **Grid**: 文章列表为不规则卡片流（left/right 交替封面方向）

## 6. Depth & Elevation

```css
--card-box-shadow: 0 3px 8px 6px rgba(7, 17, 27, 0.05);
--card-hover-box-shadow: 0 3px 8px 6px rgba(7, 17, 27, 0.09);
--menu-shadow: 0 0 1px var(--theme-color); /* 可选 */
```

- Level 0: 全屏背景
- Level 1: 毛玻璃卡片 / 导航
- Level 2: hover 阴影增强
- Level 3: 弹窗 Winbox / 搜索层

## 7. Animation & Interaction

**档位**: L2

| 效果 | 实现 |
|------|------|
| 页面加载 | `#loading-box` 双屏开合 + spinner |
| Hero 入场 | `header-effect`, `titleScale` keyframes |
| 背景淡入 | `#web_bg` `to_show` 4s |
| 文章卡片 | WOW.js `animate__zoomIn` scroll reveal |
| 副标题 | Typed.js 打字机循环 |
| 滚动 | 阅读进度条、返回顶部、导航 `show` 态 |
| Live2D | 右下角看板娘 idle |
| 侧边栏 | 抽屉滑入 `sidebarItem` |
| 暗色模式 | `data-theme="dark"` 切换 |

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

## 8. Do's and Don'ts

**Do:**
- 保持全屏壁纸 + 半透明卡片层次
- 使用 Butterfly CSS 变量体系
- 保留右侧 sidebar 小工具（作者卡、公告、友链、时钟）
- 文章卡片封面 + 摘要 + 元信息完整呈现
- 移动端折叠导航为抽屉
- 外链 CDN 保持可用（Font Awesome、jQuery 等）
- 中文内容使用 Noto Sans SC / 霞鹜文楷
- Live2D 仅在桌面端右下角展示

**Don't:**
- 不要改成纯色背景 SaaS 风
- 不要移除 `#web_bg` 全屏背景层
- 不要硬编码主题色 hex
- 不要禁用 lazyload（文章图多）
- 不要用 Emoji 替代 Font Awesome 导航图标
- 不要在大面积滚动区域使用 >14px blur
- 不要移除打字机副标题与加载动画（原站签名体验）

## 9. Responsive Behavior

| 断点 | 行为 |
|------|------|
| ≥1200px | 双栏：文章列表 + 固定 sidebar |
| 768–1199px | sidebar 下移或折叠 |
| ≤768px | 单栏；`--mobileday-bg` 背景；汉堡菜单；Live2D 缩小 |
| 触摸 | 导航/按钮最小 44×44px；取消 hover-only 功能 |

---

**参考来源**: [Kyle's Blog](https://cyborg2077.github.io/)  
**技术基底**: Hexo + Butterfly 主题 + fomal.js 魔改  
**复刻方式**: 静态镜像 `public/index.html` + 本地资源 + CDN 插件
