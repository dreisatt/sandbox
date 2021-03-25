workspace(
    name="coding_sandbox",
    managed_directories = {
        "@webserver_npm": ["web_server/node_modules"],
        "@react_npm": ["react_app/node_modules"],
    },
)
load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "rules_proto",
    sha256 = "602e7161d9195e50246177e7c55b2f39950a9cf7366f74ed5f22fd45750cd208",
    strip_prefix = "rules_proto-97d8af4dc474595af3900dd85cb3a29ad28cc313",
    urls = [
        "https://mirror.bazel.build/github.com/bazelbuild/rules_proto/archive/97d8af4dc474595af3900dd85cb3a29ad28cc313.tar.gz",
        "https://github.com/bazelbuild/rules_proto/archive/97d8af4dc474595af3900dd85cb3a29ad28cc313.tar.gz",
    ],
)
load("@rules_proto//proto:repositories.bzl", "rules_proto_dependencies", "rules_proto_toolchains")
rules_proto_dependencies()
rules_proto_toolchains()

http_archive(
    name = "io_bazel_rules_closure",
    sha256 = "d66deed38a0bb20581c15664f0ab62270af5940786855c7adc3087b27168b529",
    strip_prefix = "rules_closure-0.11.0",
    urls = ["https://github.com/bazelbuild/rules_closure/archive/0.11.0.tar.gz"],
)

http_archive(
    name = "com_github_grpc_grpc_web",
    sha256 = "8d9b1e9b839a5254aa79cb4068b05fdb6e1de5637c1b8551f95144159a4801f2",
    strip_prefix = "grpc-web-1.2.0",
    urls = ["https://github.com/grpc/grpc-web/archive/1.2.0.tar.gz"],
)

http_archive(
    name = "io_bazel_rules_go",
    sha256 = "7c10271940c6bce577d51a075ae77728964db285dac0a46614a7934dc34303e6",
    urls = [
        "https://mirror.bazel.build/github.com/bazelbuild/rules_go/releases/download/v0.26.0/rules_go-v0.26.0.tar.gz",
        "https://github.com/bazelbuild/rules_go/releases/download/v0.26.0/rules_go-v0.26.0.tar.gz",
    ],
)

load("@io_bazel_rules_go//go:deps.bzl", "go_register_toolchains", "go_rules_dependencies")

go_rules_dependencies()

go_register_toolchains(version = "1.16")

http_archive(
    name = "io_bazel_rules_webtesting",
    sha256 = "9bb461d5ef08e850025480bab185fd269242d4e533bca75bfb748001ceb343c3",
    urls = [
        "https://github.com/bazelbuild/rules_webtesting/releases/download/0.3.3/rules_webtesting.tar.gz",
    ],
)

load("@io_bazel_rules_webtesting//web:repositories.bzl", "web_test_repositories")

web_test_repositories()

######################
# Local Dependencies #
######################
new_local_repository(
   name = "GnuGsl",
   build_file = "third_party/GnuGsl.BUILD",
   path = "/usr/",
)

#########
# GTest #
#########
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
    name = "mandelbrot_deps",
    requirements = "//mandelbrot:requirements.txt",
)

load("@mandelbrot_deps//:requirements.bzl", "pip_install")

pip_install()

register_toolchains("//bazel/python:python3_only_toolchain")

###########
# Node.JS #
###########
http_archive(
    name = "build_bazel_rules_nodejs",
    sha256 = "55a25a762fcf9c9b88ab54436581e671bc9f4f523cb5a1bd32459ebec7be68a8",
    urls = ["https://github.com/bazelbuild/rules_nodejs/releases/download/3.2.2/rules_nodejs-3.2.2.tar.gz"],
)

load("@build_bazel_rules_nodejs//:index.bzl", "yarn_install")

# bazel run @nodejs_linux_amd64//:bin/node -- install/list
yarn_install(
    name = "webserver_npm",
    package_json = "//web_server:package.json",
    yarn_lock = "//web_server:yarn.lock",
)

yarn_install(
    name = "react_npm",
    package_json = "//react_app:package.json",
    yarn_lock = "//react_app:yarn.lock",
)

load("@react_npm//@bazel/labs:package.bzl", "npm_bazel_labs_dependencies")

npm_bazel_labs_dependencies()