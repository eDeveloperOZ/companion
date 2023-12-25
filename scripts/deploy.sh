#!/bin/bash

# This script checks if the current git branch is 'devel'. If it is, it ensures that the git status is clean,
# then pushes changes to the 'backup' branch. If successful, it then pushes changes to the 'main' branch.

# Get the current working directory and move up one directory level
WORK_DIR=$(pwd)
cd "$WORK_DIR/.."

# get the name of the current branch
BRANCH_NAME=$(git branch --show-current)

# Function to push changes from devel branch to given branch
push_changes() {
    local target_branch=$1
    if git push origin devel:"$target_branch";then
        echo "Pushed changes to $target_branch"
    else
        echo "Failed to push changes to $target_branch"
        exit 1
    fi
}

if [ "BRANCH_NAME" = "devel" ]; then
    echo "On devel branch"
    if [ -n "$(git status --porcelain)" ]; then
        echo "Git status is not clean, please commit changes before deploying"
        exit 1
    else
        echo "Pushing changes to backup branch"
        push_changes backup
        echo "Pushing changes to main branch"
        push_changes main
    fi
else 
    echo "Not on branch devel, please checkout devel before deploying"
    exit 1
fi