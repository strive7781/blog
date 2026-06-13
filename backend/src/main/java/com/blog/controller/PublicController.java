package com.blog.controller;

import com.blog.common.Result;
import com.blog.dto.ArticleVO;
import com.blog.dto.PageResult;
import com.blog.entity.Category;
import com.blog.entity.Tag;
import com.blog.service.ArticleService;
import com.blog.service.MetaService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/public")
@RequiredArgsConstructor
public class PublicController {

    private final ArticleService articleService;
    private final MetaService metaService;
    private final com.blog.service.SiteConfigService siteConfigService;

    @GetMapping("/articles")
    public Result<PageResult<ArticleVO>> articles(
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(required = false) Long categoryId,
            @RequestParam(required = false) Long tagId,
            @RequestParam(required = false) String keyword) {
        return Result.ok(articleService.pagePublic(page, size, categoryId, tagId, keyword));
    }

    @GetMapping("/articles/{slug}")
    public Result<ArticleVO> article(@PathVariable String slug) {
        return Result.ok(articleService.getBySlugPublic(slug));
    }

    @GetMapping("/categories")
    public Result<List<Category>> categories() {
        return Result.ok(metaService.listCategories());
    }

    @GetMapping("/tags")
    public Result<List<Tag>> tags() {
        return Result.ok(metaService.listTags());
    }

    @GetMapping("/site")
    public Result<java.util.Map<String, String>> site() {
        return Result.ok(siteConfigService.getAllMap());
    }
}
