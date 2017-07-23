ssh -i <key> ec2-user@<public-address>
sudo yum update -y
sudo yum install nginx -y
service nginx start
cd /usr/share/nginx/html/
sudo mkdir lambda-kss/
sudo yum install git -y
# add ssh public key into github
git clone git@github.com:bjpaul/lambda-sns-git-integration.git -y
cd lambda-sns-git-integration
sudo /bin/cp -rf *  /usr/share/nginx/html/lambda-kss/

