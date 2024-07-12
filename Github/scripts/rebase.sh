cd ../..
git pull origin main
git pull --rebase origin main
git add .
git commit -m "Resolved merge conflicts"
git rebase --continue
git push origin main
