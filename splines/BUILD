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
    name = "interpolation_polynomial",
    srcs = ["interpolation_polynomial.py"],
    python_version = "PY3",
    srcs_version = "PY3",
    deps = matplotlib_deps,
)

py_binary(
    name = "function_approximation_runner",
    srcs = ["lookup_table.py"],
    main = "lookup_table.py",
    python_version = "PY3",
    srcs_version = "PY3",
    deps = matplotlib_deps,
)

py_library(
    name = "cubic_spline",
    srcs = ["cubic_spline.py"],
    srcs_version = "PY3",
    deps = [
        requirement("numpy"),
        requirement("multipledispatch"),
    ]
)

py_binary(
    name = "cubic_spline_runner",
    srcs = ["cubic_spline_runner.py"],
    python_version = "PY3",
    srcs_version = "PY3",
    deps = matplotlib_deps + [":cubic_spline"],
)