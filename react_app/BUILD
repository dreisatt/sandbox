load("@react_npm//@bazel/typescript:index.bzl", "ts_library")
load("@react_npm//@bazel/concatjs:index.bzl", "concatjs_devserver")
load("@build_bazel_rules_nodejs//:index.bzl", "nodejs_binary")

ts_library(
    name = "main",
    srcs = ["main.ts"],
    tsconfig = ":tsconfig.json",
)

concatjs_devserver(
    name = "server",
    deps = [":main"],
    static_files = ["index.html"],
)