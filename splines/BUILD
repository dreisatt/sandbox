load("@splines_deps//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_binary")

matplotlib_deps = [
    requirement("matplotlib"),
    requirement("numpy"),
    requirement("kiwisolver"),
    requirement("pyparsing"),
    requirement("python-dateutil"),
    requirement("cycler"),
]

py_binary(
    name = "bezier_spline",
    srcs = ["bezier_spline.py"],
    python_version = "PY3",
    srcs_version = "PY3",
    deps = matplotlib_deps,
)

py_binary(
    name = "cubic_spline_functions",
    srcs = ["cubic_spline_functions.py"],
    python_version = "PY3",
    srcs_version = "PY3",
    deps = matplotlib_deps + [
        requirement("scipy"),
    ],
)

py_binary(
    name = "polynomial_spline",
    srcs = ["polynomial_spline.py"],
    python_version = "PY3",
    srcs_version = "PY3",
    deps = matplotlib_deps + [
        requirement("scipy"),
        requirement("sympy"),
        requirement("mpmath"),
    ],
)

py_binary(
    name = "hermite_spline",
    srcs = ["hermite_spline.py"],
    python_version = "PY3",
    srcs_version = "PY3",
    deps = matplotlib_deps,
)

py_binary(
    name = "cubic_spline",
    srcs = ["cubic_spline.py"],
    python_version = "PY3",
    srcs_version = "PY3",
    deps = matplotlib_deps + [
        requirement("multipledispatch"),
    ]
)