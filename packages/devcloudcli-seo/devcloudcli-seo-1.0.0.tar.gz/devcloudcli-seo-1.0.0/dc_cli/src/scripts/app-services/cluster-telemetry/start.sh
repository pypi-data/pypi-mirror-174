#!/bin/bash
# Copyright (C) 2018-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

#Checking kubernetes is installed or not
echo "Checking Kuberentes is installed or not"

if [[ $(which kubectl) && $(kubectl version) ]]; then
         echo -e "\e[1;32m\nKubernetes is installed\e[0m"

	 echo -e "\e[1;34m\nCreating Namespace monitoring\e[0m"
	 
	 kubectl create namespace monitoring
	 
	 echo -e "\e[1;33m\nchecking the namespace\e[0m"
	 
	 kubectl get namespace
	 
         ver=$(python3 --version | grep Python | awk '{print $2}' | xargs printf '%0.1f\n')

       	 echo -e "\e[1;32m\nCreating prometheus and grafana\e[0m"
	 
	 kubectl create -f /usr/local/lib/python$ver/dist-packages/src/scripts/app-services/cluster-telemetry/.
         
         echo -e "\e[1;36m\nChecking cluster-telemetry pods\e[0m"

	 kubectl get pods -n monitoring
     else
         echo -e "\e[1;32m\nInstall Kubernetes from devtool\e[0m"
fi


echo "If Cluster-Telemetry is working fine.Then check metrics by using Grafana"
export HOST_IP=$(hostname -I | cut -d' ' -f1)
echo -e "\e[1;32m\n********* Grafana URL **************\e[0m"
echo -e "\e[1;36mGrafana Dashboard is available in the below URL\e[0m"
echo -e "\e[1;33mhttp://$HOST_IP:32400\e[0m\n"
