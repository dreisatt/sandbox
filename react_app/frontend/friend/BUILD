package(default_visibility = ["//visibility:public"])

load("@react_npm//@bazel/typescript:index.bzl", "ts_library")

ts_library(
    name = "src",
    srcs = [
        "friend.tsx",
        "friend-service.ts"
    ],
    tsconfig = "//react_app:tsconfig.json",
    deps = [
        "//react_app/model",
        "//react_app/frontend/config",
        "@react_npm//react",
        "@react_npm//@types/react",
    ]
)