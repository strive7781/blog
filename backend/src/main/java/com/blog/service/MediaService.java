package com.blog.service;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.blog.config.UploadProperties;
import com.blog.dto.PageResult;
import com.blog.entity.Media;
import com.blog.mapper.MediaMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class MediaService {

    private final MediaMapper mediaMapper;
    private final UploadProperties uploadProperties;

    public Media upload(MultipartFile file) throws IOException {
        String ext = "";
        String original = file.getOriginalFilename();
        if (original != null && original.contains(".")) {
            ext = original.substring(original.lastIndexOf('.'));
        }
        String dateDir = LocalDate.now().format(DateTimeFormatter.ofPattern("yyyy/MM"));
        Path dir = Paths.get(uploadProperties.getDir(), dateDir);
        Files.createDirectories(dir);
        String filename = UUID.randomUUID().toString().replace("-", "") + ext;
        Path target = dir.resolve(filename);
        file.transferTo(target.toFile());

        String url = uploadProperties.getUrlPrefix() + "/" + dateDir + "/" + filename;
        Media media = new Media();
        media.setFilename(original != null ? original : filename);
        media.setUrl(url);
        media.setMimeType(file.getContentType());
        media.setSizeBytes(file.getSize());
        mediaMapper.insert(media);
        return media;
    }

    public PageResult<Media> page(int page, int size) {
        Page<Media> p = mediaMapper.selectPage(new Page<>(page, size),
                new LambdaQueryWrapper<Media>().orderByDesc(Media::getCreatedAt));
        return PageResult.of(p.getTotal(), page, size, p.getRecords());
    }

    public void delete(Long id) {
        mediaMapper.deleteById(id);
    }
}
