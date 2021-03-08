workspace(name="coding_sandbox")
load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

new_local_repository(
   name = "GnuGsl",
   build_file = "third_party/GnuGsl.BUILD",
   path = "/usr/",
)

git_repository(
   name = "gtest",
   remote = "https://github.com/google/googletest",
   tag = "release-1.10.0",
)

##################
# Python runtime #
##################
git_repository(
    name = "rules_python",
    remote = "https://github.com/bazelbuild/rules_python.git",
    commit = "06672cd470ce513a256c7ef2dbb8497a0f5502f3",
)

load("@rules_python//python:repositories.bzl", "py_repositories")

py_repositories()

load("@rules_python//python:pip.bzl", "pip_repositories")

pip_repositories()

load("@rules_python//python:pip.bzl", "pip_import")

pip_import(
    name = "py_deps",
    requirements = "//mandelbrot:requirements.txt",
)

load("@py_deps//:requirements.bzl", "pip_install")

pip_install()

register_toolchains("//mandelbrot:my_py_toolchain")