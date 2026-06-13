package com.blog.dto;

import lombok.Data;

@Data
public class PageResult<T> {
    private long total;
    private long page;
    private long size;
    private java.util.List<T> records;

    public static <T> PageResult<T> of(long total, long page, long size, java.util.List<T> records) {
        PageResult<T> r = new PageResult<>();
        r.total = total;
        r.page = page;
        r.size = size;
        r.records = records;
        return r;
    }
}
