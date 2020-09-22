#!/bin/bash

# Additionally certbot will pass relevant environment variables as below:
# CERTBOT_DOMAIN: The domain being authenticated
# CERTBOT_VALIDATION: The validation string
# CERTBOT_TOKEN: Resource name part of the HTTP-01 challenge (HTTP-01 only)
# CERTBOT_REMAINING_CHALLENGES: Number of challenges remaining after the current challenge
# CERTBOT_ALL_DOMAINS: A comma-separated list of all domains challenged for the current certificate
if [ -z "$CERTBOT_DOMAIN" ]
then
  CERTBOT_DOMAIN="celerysoft.com"
fi
if [ -z "$CERTBOT_VALIDATION" ]
then
  CERTBOT_VALIDATION="abcdefghijklmnopqrstuvwxyz"
fi

PATH=$(cd `dirname $0`; pwd)

# 可能需要修改一下 PYTHONPATH，如果python环境不在当前目录下的话
PYTHONPATH=""
if [ -z "$PYTHONPATH" ]
then
  PYTHONPATH=$PATH
fi
export PYTHONPATH

# 可能需要修改一下 cmd，如果没使用虚拟环境的话，或者虚拟环境不在当前目录下
cmd="${PATH}/venv/bin/python ${PATH}/auth.py"

$cmd $CERTBOT_DOMAIN "_acme-challenge" $CERTBOT_VALIDATION
