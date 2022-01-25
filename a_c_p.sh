git add .
echo "Commit message:"
read message
git commit -m "$message"
echo "Branch name (default: master)"
read branchName
cat ~/github_oAuth
git push origin $branchName

