hash=`md5sum ./requirements.in | cut -c 1-16`
docker build -f Dockerfile.dev -t swxs/home_base:$hash . 
docker push swxs/home_base:$hash
docker image tag swxs/home_base:$hash swxs/home_base:latest
docker push swxs/home_base:latest
