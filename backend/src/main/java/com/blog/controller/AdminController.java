package com.blog.controller;

import com.blog.common.Result;
import com.blog.entity.Category;
import com.blog.entity.Media;
import com.blog.entity.Tag;
import com.blog.dto.PageResult;
import com.blog.service.MediaService;
import com.blog.service.MetaService;
import com.blog.service.SiteConfigService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/admin")
@RequiredArgsConstructor
public class AdminController {

    private final MetaService metaService;
    private final MediaService mediaService;
    private final SiteConfigService siteConfigService;

    @GetMapping("/categories")
    public Result<List<Category>> categories() {
        return Result.ok(metaService.listCategories());
    }

    @PostMapping("/categories")
    public Result<Category> saveCategory(@RequestBody Category category) {
        return Result.ok(metaService.saveCategory(category));
    }

    @DeleteMapping("/categories/{id}")
    public Result<Void> deleteCategory(@PathVariable Long id) {
        metaService.deleteCategory(id);
        return Result.ok();
    }

    @GetMapping("/tags")
    public Result<List<Tag>> tags() {
        return Result.ok(metaService.listTags());
    }

    @PostMapping("/tags")
    public Result<Tag> saveTag(@RequestBody Tag tag) {
        return Result.ok(metaService.saveTag(tag));
    }

    @DeleteMapping("/tags/{id}")
    public Result<Void> deleteTag(@PathVariable Long id) {
        metaService.deleteTag(id);
        return Result.ok();
    }

    @PostMapping("/media/upload")
    public Result<Media> upload(@RequestParam("file") MultipartFile file) throws IOException {
        return Result.ok(mediaService.upload(file));
    }

    @GetMapping("/media")
    public Result<PageResult<Media>> media(
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "20") int size) {
        return Result.ok(mediaService.page(page, size));
    }

    @DeleteMapping("/media/{id}")
    public Result<Void> deleteMedia(@PathVariable Long id) {
        mediaService.delete(id);
        return Result.ok();
    }

    @GetMapping("/site")
    public Result<Map<String, String>> getSite() {
        return Result.ok(siteConfigService.getAllMap());
    }

    @PutMapping("/site")
    public Result<Void> saveSite(@RequestBody Map<String, String> configs) {
        siteConfigService.saveAll(configs);
        return Result.ok();
    }
}
