package com.blog.service;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.blog.common.BusinessException;
import com.blog.dto.ArticleRequest;
import com.blog.dto.ArticleVO;
import com.blog.dto.PageResult;
import com.blog.dto.TagVO;
import com.blog.entity.Article;
import com.blog.entity.Category;
import com.blog.entity.Tag;
import com.blog.mapper.ArticleMapper;
import com.blog.mapper.ArticleTagMapper;
import com.blog.mapper.CategoryMapper;
import com.blog.mapper.TagMapper;
import com.blog.util.SlugUtil;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.util.StringUtils;

import java.time.LocalDateTime;
import java.util.*;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class ArticleService {

    private final ArticleMapper articleMapper;
    private final CategoryMapper categoryMapper;
    private final TagMapper tagMapper;
    private final ArticleTagMapper articleTagMapper;

    public PageResult<ArticleVO> pagePublic(int page, int size, Long categoryId, Long tagId, String keyword) {
        return pageInternal(page, size, categoryId, tagId, keyword, 1);
    }

    public PageResult<ArticleVO> pageAdmin(int page, int size, Integer status, String keyword) {
        LambdaQueryWrapper<Article> qw = new LambdaQueryWrapper<>();
        if (status != null) {
            qw.eq(Article::getStatus, status);
        }
        if (StringUtils.hasText(keyword)) {
            qw.and(w -> w.like(Article::getTitle, keyword).or().like(Article::getSummary, keyword));
        }
        qw.orderByDesc(Article::getUpdatedAt);
        Page<Article> p = articleMapper.selectPage(new Page<>(page, size), qw);
        List<ArticleVO> list = p.getRecords().stream().map(this::toVoWithoutContent).toList();
        return PageResult.of(p.getTotal(), page, size, list);
    }

    private PageResult<ArticleVO> pageInternal(int page, int size, Long categoryId, Long tagId, String keyword, int status) {
        LambdaQueryWrapper<Article> qw = new LambdaQueryWrapper<>();
        qw.eq(Article::getStatus, status);
        if (categoryId != null) {
            qw.eq(Article::getCategoryId, categoryId);
        }
        if (StringUtils.hasText(keyword)) {
            qw.and(w -> w.like(Article::getTitle, keyword).or().like(Article::getSummary, keyword));
        }
        qw.orderByDesc(Article::getPublishedAt);
        Page<Article> p = articleMapper.selectPage(new Page<>(page, size), qw);
        List<ArticleVO> list = p.getRecords().stream().map(this::toVoWithoutContent).toList();
        if (tagId != null) {
            list = list.stream().filter(vo -> vo.getTags().stream().anyMatch(t -> t.getId().equals(tagId))).toList();
        }
        return PageResult.of(p.getTotal(), page, size, list);
    }

    public ArticleVO getBySlugPublic(String slug) {
        Article article = articleMapper.selectOne(new LambdaQueryWrapper<Article>()
                .eq(Article::getSlug, slug).eq(Article::getStatus, 1));
        if (article == null) {
            throw new BusinessException("文章不存在");
        }
        article.setViewCount(article.getViewCount() + 1);
        articleMapper.updateById(article);
        return toVo(article);
    }

    public ArticleVO getByIdAdmin(Long id) {
        Article article = articleMapper.selectById(id);
        if (article == null) {
            throw new BusinessException("文章不存在");
        }
        return toVo(article);
    }

    @Transactional
    public ArticleVO create(ArticleRequest req) {
        Article article = new Article();
        fillArticle(article, req, true);
        articleMapper.insert(article);
        saveTags(article.getId(), req.getTagIds());
        return toVo(article);
    }

    @Transactional
    public ArticleVO update(Long id, ArticleRequest req) {
        Article article = articleMapper.selectById(id);
        if (article == null) {
            throw new BusinessException("文章不存在");
        }
        fillArticle(article, req, false);
        articleMapper.updateById(article);
        articleTagMapper.deleteByArticleId(id);
        saveTags(id, req.getTagIds());
        return toVo(article);
    }

    @Transactional
    public void delete(Long id) {
        articleTagMapper.deleteByArticleId(id);
        articleMapper.deleteById(id);
    }

    private void fillArticle(Article article, ArticleRequest req, boolean isNew) {
        article.setTitle(req.getTitle());
        article.setSlug(StringUtils.hasText(req.getSlug()) ? req.getSlug() : SlugUtil.toSlug(req.getTitle()));
        article.setSummary(req.getSummary());
        article.setContentMd(req.getContentMd());
        article.setCoverUrl(req.getCoverUrl());
        article.setCategoryId(req.getCategoryId());
        article.setStatus(req.getStatus() != null ? req.getStatus() : 0);
        if (article.getStatus() == 1) {
            article.setPublishedAt(req.getPublishedAt() != null ? req.getPublishedAt() : LocalDateTime.now());
        }
        if (isNew) {
            article.setViewCount(0);
        }
        ensureUniqueSlug(article.getSlug(), isNew ? null : article.getId());
    }

    private void ensureUniqueSlug(String slug, Long excludeId) {
        LambdaQueryWrapper<Article> qw = new LambdaQueryWrapper<Article>().eq(Article::getSlug, slug);
        if (excludeId != null) {
            qw.ne(Article::getId, excludeId);
        }
        if (articleMapper.selectCount(qw) > 0) {
            throw new BusinessException("slug 已存在: " + slug);
        }
    }

    private void saveTags(Long articleId, List<Long> tagIds) {
        if (tagIds == null) return;
        for (Long tagId : new LinkedHashSet<>(tagIds)) {
            articleTagMapper.insert(articleId, tagId);
        }
    }

    private ArticleVO toVoWithoutContent(Article article) {
        ArticleVO vo = toVo(article);
        vo.setContentMd(null);
        return vo;
    }

    private ArticleVO toVo(Article article) {
        ArticleVO vo = new ArticleVO();
        vo.setId(article.getId());
        vo.setTitle(article.getTitle());
        vo.setSlug(article.getSlug());
        vo.setSummary(article.getSummary());
        vo.setContentMd(article.getContentMd());
        vo.setCoverUrl(article.getCoverUrl());
        vo.setCategoryId(article.getCategoryId());
        vo.setStatus(article.getStatus());
        vo.setViewCount(article.getViewCount());
        vo.setPublishedAt(article.getPublishedAt());
        vo.setCreatedAt(article.getCreatedAt());
        vo.setUpdatedAt(article.getUpdatedAt());
        if (article.getCategoryId() != null) {
            Category c = categoryMapper.selectById(article.getCategoryId());
            if (c != null) vo.setCategoryName(c.getName());
        }
        List<Long> tagIds = articleTagMapper.findTagIdsByArticleId(article.getId());
        if (!tagIds.isEmpty()) {
            List<Tag> tags = tagMapper.selectBatchIds(tagIds);
            vo.setTags(tags.stream().map(t -> {
                TagVO tv = new TagVO();
                tv.setId(t.getId());
                tv.setName(t.getName());
                tv.setSlug(t.getSlug());
                return tv;
            }).toList());
        } else {
            vo.setTags(List.of());
        }
        return vo;
    }
}
