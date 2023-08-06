#!/bin/bash

echo "-------------------------------------------------------"
echo -e "\e[1;36mUninstalling Kubernetes Dashboard..\e[0m"

kubectl delete -f $PWD/kubernetes-dashboard/
sleep 5s

echo "-------------------------------------------------------"
echo -e "\e[1;36mUninstalled Successfully\e[0m"

