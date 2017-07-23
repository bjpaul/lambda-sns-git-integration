#!/bin/sh
sudo yum update -y
cd lambda-sns-git-integration
echo "Pulling latest changes"
git pull origin master
echo "Copying files"
sudo /bin/cp -rf *  /usr/share/nginx/html/lambda-kss/
