load("@react_npm//@bazel/typescript:index.bzl", "ts_library")
load("@react_npm//@bazel/concatjs:index.bzl", "concatjs_devserver")
load("@build_bazel_rules_nodejs//:index.bzl", "nodejs_binary")
load("@react_npm//http-server:index.bzl", "http_server")

ts_library(
    name = "main",
    srcs = ["main.ts"],
    tsconfig = ":tsconfig.json",
)

concatjs_devserver(
    name = "server",
    deps = [":main"]
)

concatjs_devserver(
    name = "devserver",
    # We'll collect all the devmode JS sources from these TypeScript libraries
    deps = [":main"],
    # This is the path we'll request from the browser, see index.html
    # serving_path = "/bundle.js",
    # The devserver can serve our static files too
    static_files = ["index.html"],
)

# http_server(
#     name = "server",
#     data = [
#         ":index.html",
#         ":main",
#     ],
#     templated_args = ["main"],
# )