package com.blog.service;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.blog.common.BusinessException;
import com.blog.entity.Category;
import com.blog.entity.Tag;
import com.blog.mapper.CategoryMapper;
import com.blog.mapper.TagMapper;
import com.blog.util.SlugUtil;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

import java.util.List;

@Service
@RequiredArgsConstructor
public class MetaService {

    private final CategoryMapper categoryMapper;
    private final TagMapper tagMapper;

    public List<Category> listCategories() {
        return categoryMapper.selectList(new LambdaQueryWrapper<Category>().orderByAsc(Category::getSortOrder));
    }

    public Category saveCategory(Category category) {
        if (!StringUtils.hasText(category.getSlug())) {
            category.setSlug(SlugUtil.toSlug(category.getName()));
        }
        if (category.getId() == null) {
            categoryMapper.insert(category);
        } else {
            categoryMapper.updateById(category);
        }
        return category;
    }

    public void deleteCategory(Long id) {
        categoryMapper.deleteById(id);
    }

    public List<Tag> listTags() {
        return tagMapper.selectList(new LambdaQueryWrapper<Tag>().orderByAsc(Tag::getName));
    }

    public Tag saveTag(Tag tag) {
        if (!StringUtils.hasText(tag.getSlug())) {
            tag.setSlug(SlugUtil.toSlug(tag.getName()));
        }
        if (tag.getId() == null) {
            tagMapper.insert(tag);
        } else {
            tagMapper.updateById(tag);
        }
        return tag;
    }

    public void deleteTag(Long id) {
        tagMapper.deleteById(id);
    }
}
