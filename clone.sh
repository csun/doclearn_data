cd repos
git clone --depth=1 $1
REPO_NAME=${1##*/}

cd $REPO_NAME
COMMIT_HASH=$(git rev-parse HEAD)

cd ../../repo_data
echo "{ \"repo_url\": \"$1\", \"commit_hash\": \"$COMMIT_HASH\" }" >> $REPO_NAME.json
