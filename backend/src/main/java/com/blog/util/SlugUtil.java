package com.blog.util;

import java.text.Normalizer;
import java.util.Locale;
import java.util.regex.Pattern;

public final class SlugUtil {
    private static final Pattern NON_LATIN = Pattern.compile("[^\\w-]");
    private static final Pattern WHITESPACE = Pattern.compile("[\\s]");

    private SlugUtil() {}

    public static String toSlug(String input) {
        if (input == null || input.isBlank()) {
            return "post-" + System.currentTimeMillis();
        }
        String nowhitespace = WHITESPACE.matcher(input).replaceAll("-");
        String normalized = Normalizer.normalize(nowhitespace, Normalizer.Form.NFD);
        String slug = NON_LATIN.matcher(normalized).replaceAll("");
        slug = slug.toLowerCase(Locale.ROOT).replaceAll("-{2,}", "-").replaceAll("^-|-$", "");
        return slug.isBlank() ? "post-" + System.currentTimeMillis() : slug;
    }
}
