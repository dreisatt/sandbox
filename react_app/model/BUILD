package(default_visibility = ["//visibility:public"])
load("@rules_proto//proto:defs.bzl", "proto_library")
load("@react_npm//@bazel/typescript:index.bzl", "ts_library")
load("@react_npm//@bazel/labs:index.bzl", "ts_proto_library")

proto_library(
    name = "friend_proto",
    srcs = ["friend.proto"],
)

ts_proto_library(
    name = "friend_ts_proto",
    proto = ":friend_proto",
)

ts_library(
    name = "model",
    srcs = ["index.ts"],
    tsconfig = "//react_app:tsconfig.json",
    deps = [":friend_ts_proto"]
)