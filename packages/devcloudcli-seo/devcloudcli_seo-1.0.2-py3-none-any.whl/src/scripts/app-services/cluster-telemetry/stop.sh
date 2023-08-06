#!/bin/bash
# Copyright (C) 2018-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

ver=$(python3 --version | grep Python | awk '{print $2}' | xargs printf '%0.1f\n')

echo -e "\e[1;32m\nDeleting prometheus and grafana\e[0m"

kubectl delete -f /usr/local/lib/python$ver/dist-packages/src/scripts/app-services/cluster-telemetry/.

echo -e "\e[1;36m\nDeleting Namespace\e[0m"

kubectl delete namespace monitoring

echo -e "\e[1;34m\nChecking Namespace\e[0m"

kubectl get namespace


