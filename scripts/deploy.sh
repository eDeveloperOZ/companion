#!/bin/bash

# This script checks if the current git branch is 'devel'. If it is, it ensures that the git status is clean,
# then pushes changes from 'devel' to 'main' and from 'main' to 'backup'.

# Get the current working directory and move up one directory level
WORK_DIR=$(pwd)
cd "$WORK_DIR/.."
BRANCH_NAME=$(git branch --show-current)

# Function to push changes from one branch to another
push_changes() {
    local source_branch=$1
    local target_branch=$2
    if git push origin "$source_branch":"$target_branch"; then
        echo "Pushed changes from $source_branch to $target_branch"
    else
        echo "Failed to push changes from $source_branch to $target_branch"
        exit 1
    fi
}

if [ "$BRANCH_NAME" = "devel" ]; then
    echo "On devel branch"
    if [ -n "$(git status --porcelain)" ]; then
        echo "Git status is not clean, please commit changes before deploying"
        exit 1
    else
        echo "Pushing changes from main to backup"
        git merge main backup
        echo "Pushing changes from devel to main"
        push_changes devel main
    fi
else
    echo "Not on branch devel, please checkout devel before deploying"
    exit 1
fi
