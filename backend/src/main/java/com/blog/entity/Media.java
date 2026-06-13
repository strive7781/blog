package com.blog.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.time.LocalDateTime;

@Data
@TableName("media")
public class Media {
    @TableId(type = IdType.AUTO)
    private Long id;
    private String filename;
    private String url;
    private String mimeType;
    private Long sizeBytes;
    private LocalDateTime createdAt;
}
