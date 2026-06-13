package com.blog.mapper;

import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface ArticleTagMapper {

    @Insert("INSERT INTO article_tag (article_id, tag_id) VALUES (#{articleId}, #{tagId})")
    void insert(Long articleId, Long tagId);

    @Delete("DELETE FROM article_tag WHERE article_id = #{articleId}")
    void deleteByArticleId(Long articleId);

    @Select("SELECT tag_id FROM article_tag WHERE article_id = #{articleId}")
    List<Long> findTagIdsByArticleId(Long articleId);
}
