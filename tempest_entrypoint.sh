#!/bin/bash -x
cd /tempest
source testbed_env
chmod +x tempest_run.sh
/tempest/tempest_run.sh
cp result*.xml ./logs
cp build_id.txt ./logs
