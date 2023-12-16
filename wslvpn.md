cat /etc/resolv.conf
export https_proxy="http://8.8.8.8:33210
unset https_proxy

git config --global https.proxy 0.0.0.0:33210
git config --global --unset https.proxy