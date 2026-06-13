package com.blog.service;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.blog.entity.SiteConfig;
import com.blog.mapper.SiteConfigMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

@Service
@RequiredArgsConstructor
public class SiteConfigService {

    private final SiteConfigMapper siteConfigMapper;

    public Map<String, String> getAllMap() {
        List<SiteConfig> list = siteConfigMapper.selectList(null);
        Map<String, String> map = new LinkedHashMap<>();
        for (SiteConfig c : list) {
            map.put(c.getConfigKey(), c.getConfigValue());
        }
        return map;
    }

    public void saveAll(Map<String, String> configs) {
        for (Map.Entry<String, String> e : configs.entrySet()) {
            SiteConfig existing = siteConfigMapper.selectOne(
                    new LambdaQueryWrapper<SiteConfig>().eq(SiteConfig::getConfigKey, e.getKey()));
            if (existing != null) {
                existing.setConfigValue(e.getValue());
                siteConfigMapper.updateById(existing);
            } else {
                SiteConfig c = new SiteConfig();
                c.setConfigKey(e.getKey());
                c.setConfigValue(e.getValue());
                siteConfigMapper.insert(c);
            }
        }
    }
}
