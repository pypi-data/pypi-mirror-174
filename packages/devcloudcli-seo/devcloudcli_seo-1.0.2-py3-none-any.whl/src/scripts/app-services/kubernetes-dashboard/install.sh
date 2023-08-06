#!/bin/bash

echo "-------------------------------------------------------"
echo -e "\e[1;36mDeploying Kubernetes Dashboard..\e[0m"

kubectl apply -f $PWD/kubernetes-dashboard/
sleep 5s

echo "-------------------------------------------------------"
echo
echo "-------------------------------------------------------"
echo -e "\e[1;36mFetching Dashboard Details..\e[0m"

export DASH_NODE_IP=`kubectl get nodes -o wide | grep -E '[0-9]' | awk {'print $6'}`
export DASH_NODE_PORT=`kubectl get svc -A |grep kubernetes-dashboard |grep 443 | sed  's/443//' |sed  's/\TCP//' |awk {'print $6'}`

echo "-------------------------------------------------------"
echo "Your Dashboard with Nodeport URL is: https://$DASH_NODE_IP$DASH_NODE_PORT"
echo "-------------------------------------------------------"
echo


echo "-------------------------------------------------------"
echo "ADMIN TOKEN DETAILS"
echo
kubectl -n kubernetes-dashboard describe secret $(kubectl -n kubernetes-dashboard get secret | grep admin-user | awk '{print $1}')
echo "-------------------------------------------------------"

