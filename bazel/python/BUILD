py_runtime(
    name = "python3_runtime",
    interpreter_path = "/usr/bin/python3",
    python_version = "PY3",
    visibility = ["//visibility:public"],
)

load("@rules_python//python:defs.bzl", "py_runtime_pair")

py_runtime_pair(
    name = "py3_only_runtime_pair",
    py2_runtime = None,
    py3_runtime = ":python3_runtime",
)

toolchain(
    name = "python3_only_toolchain",
    toolchain = ":py3_only_runtime_pair",
    toolchain_type = "@bazel_tools//tools/python:toolchain_type",
)