cc_library(
    name = "sorting",
    srcs = ["src/sort.cpp"],
    hdrs = ["include/sorting/sort.h"],
    strip_include_prefix = "include",
)

cc_test(
    name = "sorting_spec",
    srcs = ["test/sort_spec.cpp"],
    deps = [
        ":sorting",
        "@gtest//:gtest",
        "@gtest//:gtest_main",
    ]
)