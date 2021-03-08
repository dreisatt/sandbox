cc_library(name = "spin_lock", srcs = ["spin_lock.cpp"], hdrs = ["spin_lock.hpp"], )

    cc_test(name = "spin_lock_spec", srcs = ["test/spin_lock_spec.cpp"], deps = [
      "@gtest//:gtest_main",
      "//multi_threading:spin_lock",
    ], )