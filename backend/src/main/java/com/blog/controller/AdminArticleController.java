package com.blog.controller;

import com.blog.common.Result;
import com.blog.dto.ArticleRequest;
import com.blog.dto.ArticleVO;
import com.blog.dto.PageResult;
import com.blog.service.ArticleService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/admin/articles")
@RequiredArgsConstructor
public class AdminArticleController {

    private final ArticleService articleService;

    @GetMapping
    public Result<PageResult<ArticleVO>> page(
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(required = false) Integer status,
            @RequestParam(required = false) String keyword) {
        return Result.ok(articleService.pageAdmin(page, size, status, keyword));
    }

    @GetMapping("/{id}")
    public Result<ArticleVO> detail(@PathVariable Long id) {
        return Result.ok(articleService.getByIdAdmin(id));
    }

    @PostMapping
    public Result<ArticleVO> create(@Valid @RequestBody ArticleRequest req) {
        return Result.ok(articleService.create(req));
    }

    @PutMapping("/{id}")
    public Result<ArticleVO> update(@PathVariable Long id, @Valid @RequestBody ArticleRequest req) {
        return Result.ok(articleService.update(id, req));
    }

    @DeleteMapping("/{id}")
    public Result<Void> delete(@PathVariable Long id) {
        articleService.delete(id);
        return Result.ok();
    }
}
