#!/bin/bash

repo_dir=$(git rev-parse --show-toplevel)
cp -r $repo_dir/git-hooks/hooks/* $repo_dir/.git/hooks
chmod +x $repo_dir/.git/hooks
