package com.blog.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;

import java.time.LocalDateTime;
import java.util.List;

@Data
public class ArticleRequest {
    @NotBlank
    private String title;
    private String slug;
    private String summary;
    @NotBlank
    private String contentMd;
    private String coverUrl;
    private Long categoryId;
    private Integer status;
    private List<Long> tagIds;
    private LocalDateTime publishedAt;
}
