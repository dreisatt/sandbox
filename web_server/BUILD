load("@build_bazel_rules_nodejs//:index.bzl", "nodejs_binary")

filegroup(
    name = "web_server_assets",
    srcs = [
        "root/index.html",
        "root/js/main.js",
        "root/images/richard_wolf_logo.jpeg",
    ],
)

nodejs_binary(
    name = "web_server",
    entry_point = ":server.js",
    data = [
        "@webserver_npm//http",
        "@webserver_npm//fs",
        "@webserver_npm//path",
        "@webserver_npm//url",
        ":web_server_assets",
    ],
)