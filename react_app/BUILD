load("@react_npm//@bazel/typescript:index.bzl", "ts_library")
load("@react_npm//@bazel/concatjs:index.bzl", "concatjs_devserver")
load("@build_bazel_rules_nodejs//:index.bzl", "nodejs_binary")
load("@react_npm//@bazel/rollup:index.bzl", "rollup_bundle")

exports_files([
  "tsconfig.json",
])

ts_library(
    name = "main",
    srcs = [
        "frontend/main.tsx",
        "frontend/app.tsx",
    ],
    tsconfig = ":tsconfig.json",
    deps = [
        "//react_app/frontend/friend:src",
        "//react_app/model",
        "@react_npm//react",
        "@react_npm//react-dom",
        "@react_npm//@types/react",
        "@react_npm//@types/react-dom",
    ]
)

rollup_bundle(
    name = "bundle",
    entry_point = "frontend/main.tsx",
    deps = [
        ":main",
        "@react_npm//react",
        "@react_npm//react-dom",
    ],
)

concatjs_devserver(
    name = "devserver",
    additional_root_paths = [
        "npm/node_modules/react/umd",
        "npm/node_modules/react-dom/umd",
    ],
    deps = [":bundle"],
    port = 8081,
    serving_path = "/bundle.js",
    static_files = [
        ":main",
        ":index.html",
        ":bundle",
        "//react_app/styles:styles",
    ],
)