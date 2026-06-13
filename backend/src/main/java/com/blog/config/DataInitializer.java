package com.blog.config;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.blog.entity.AdminUser;
import com.blog.mapper.AdminUserMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class DataInitializer implements CommandLineRunner {

    private final AdminUserMapper adminUserMapper;
    private final BCryptPasswordEncoder encoder = new BCryptPasswordEncoder();

    @Override
    public void run(String... args) {
        AdminUser existing = adminUserMapper.selectOne(
                new LambdaQueryWrapper<AdminUser>().eq(AdminUser::getUsername, "admin"));
        if (existing == null) {
            AdminUser admin = new AdminUser();
            admin.setUsername("admin");
            admin.setPassword(encoder.encode("admin123"));
            admin.setNickname("管理员");
            adminUserMapper.insert(admin);
        }
    }
}
