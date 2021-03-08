load("@py_deps//:requirements.bzl", "requirement")

py_runtime(
    name = "python3_runtime",
    interpreter_path = "/usr/bin/python3",
    python_version = "PY3",
    visibility = ["//visibility:public"],
)

load("@rules_python//python:defs.bzl", "py_runtime_pair")

py_runtime_pair(
    name = "my_py_runtime_pair",
    py2_runtime = None,
    py3_runtime = ":python3_runtime",
)

toolchain(
    name = "my_py_toolchain",
    toolchain = ":my_py_runtime_pair",
    toolchain_type = "@bazel_tools//tools/python:toolchain_type",
)

py_binary(
    name = "mandelbrot",
    srcs = ["mandelbrot.py"],
    python_version = "PY3",
    srcs_version = "PY3",
    deps = [
        requirement("matplotlib"),
        requirement("pyparsing"),
        requirement("cycler"),
        requirement("numpy"),
        requirement("kiwisolver"),
        requirement("python-dateutil"),
        requirement("pillow"),
    ],
)