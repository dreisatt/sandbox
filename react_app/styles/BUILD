package(default_visibility = ["//visibility:public"])

load("@react_npm//sass:index.bzl", "sass")

sass(
    name = "styles",
    outs = ["styles.css"],
    args = [
        "$(execpath styles.scss)",
        "$(execpath styles.css)",
    ],
    data = ["styles.scss"],
)