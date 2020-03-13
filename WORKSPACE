load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")

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
