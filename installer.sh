#!/usr/bin/bash
# 
# configs
# 

# PLEASE DELETE .git BEFORE USE

# lock unlock configs
is_configured=true
docker_image_name="fuel_parser_image"
docker_container_name="fuel_parser_container"
docker_port_outside=9011   # check Dockerfile EXPOSE and script to start dev and prod server before
docker_port_inside=9011    # check Dockerfile EXPOSE and script to start dev and prod server before

# 
# check for configured
# 

if [ $is_configured == true ]
then

# 
# main app loop
# 

while [ true ]
do
# clean console
clear

# controll message
echo "ESC: exit"
echo "1: star dev server"
echo "2: start prod server"
echo "7: install docker"
echo "8: delete docker"

# read user key
read -sn 1 key

# if escape break loop
if [ "$key" = $'\e' ]
then
break
fi

# dev server
if [ "$key" = "1" ]
then
clear
./dev_start.sh
break
fi

# prod server
if [ "$key" = "2" ]
then
clear
./prod_start.sh
break
fi

# Docker installing
if [ "$key" = "7" ]
then
clear

# build new image and run app
docker build -t $docker_image_name .
docker run -dit -p $docker_port_outside:$docker_port_inside --name $docker_container_name $docker_image_name

echo "Docker container installed"
break
fi

# Docker removing
if [ "$key" = "8" ]
then
clear

docker container stop $docker_container_name
docker container rm $docker_container_name
docker image rm $docker_image_name

echo "Docker image and container was removed"
break
fi

# stop loop
done

# Show message is not configured
else
clear
echo "Before use, please config this file and set variable 'is_configured=true'"
fi