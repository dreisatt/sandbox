load("@splines_deps//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_binary")

py_binary(
    name = "bezier_spline",
    srcs = ["bezier_spline.py"],
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