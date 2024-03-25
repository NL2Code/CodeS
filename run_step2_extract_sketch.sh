#!/bin/bash
# Copyright (c) Huawei Cloud.
# Licensed under the MIT license.

BASE_PATH="./cleaned_repos/"
OUTPUT_PATH="./outputs/"
# Delete all files in the output path
rm -rf $OUTPUT_PATH/*

REPO_NAMEs="snake-ai-master,big-list-of-naughty-strings-master,PySnooper-master,Photon-master,icecream-master,TrumpScript-master,latexify_py-main,maybe-master,autoscraper-master,vibora-master,peda-master,httpstat-master,whereami-master,acme-tiny-master,Arjun-master,better-exceptions-master,arxiv-latex-cleaner-main,open-interpreter-main,Depix-main"
REPO_NAMEs="$REPO_NAMEs,pytorch-captcha-recognition-master,simple-neural-network-master,gorilla-cli-main,cachebrowser-master,FlapPyBird-master,waf-bypass-master,Silver-master,CTags-development,RSS-to-Telegram-Bot-dev,Instabruteforce-master,ANGRYsearch-master,ddt4all-master"
REPO_NAMEs="$REPO_NAMEs,trzsz-main,Min_Max_Similarity-main,Bg-mini-master,fastapi-cache-main,Shreddit-master,aws-mfa-master,cmdb-master,LazyIDA-master,aws-cfn-template-flip-master,tissue-master,sublert-master,Brightness-master,susi_api-master,BlackMamba-main"
REPO_NAMEs="$REPO_NAMEs,flask-ln-main,jwt_tool-master,knock-master,pypush-main,robobrowser-master,3d-ken-burns-master,cloudpickle-master,django-admin-interface-main,dominate-master,flask-jwt-extended-master,ouroboros-master,ps_mem-master,pyperclip-master,python-bloomfilter-master,ROADtools-master,xlsx2csv-master"
REPO_NAMEs="$REPO_NAMEs,apiflask-main,autotab-starter-main,clean-text-main,django-annoying-master,DumpsterDiver-master,firefox_decrypt-main,heartrate-master,makesite-master,mochi-master,oj-master,orm-master,python-email-validator-main,python-string-similarity-master,PythonVerbalExpressions-master,requestium-master,SecretFinder-master,SimpleCoin-master,SubDomainizer-master,tldextract-master"
REPO_NAMEs="$REPO_NAMEs,CloakQuest3r-main,csvs-to-sqlite-main,django-solo-master,elasticsearch-gmail-master,exrex-master,fastapi-code-generator-master,feincms-main,handout-master,htpwdScan-master,Microsoft-Rewards-Farmer-master,nvpy-master,pyment-master,python-exe-unpacker-master,Reconnoitre-master,RedditStorage-master,snallygaster-main,stocktalk-master,Striker-master,thefuzz-master"

Run_Command_Args=" --base_path $BASE_PATH"
Run_Command_Args="$Run_Command_Args --repo_names $REPO_NAMEs"
Run_Command_Args="$Run_Command_Args --output_path $OUTPUT_PATH"

echo "Run Command Args: $Run_Command_Args"

python extract_sketch.py $Run_Command_Args