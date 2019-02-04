#!/bin/bash

IAM_FOLDER=./data/iam

mkdir -p $IAM_FOLDER
mkdir -p $IAM_FOLDER/ascii
mkdir -p $IAM_FOLDER/words

user=$1
pwd=$2

echo "Downloading IAM words for $1..."

wget -N -P $IAM_FOLDER --user="$user" --password="$pwd" http://www.fki.inf.unibe.ch/DBs/iamDB/data/words/words.tgz
wget -N -P $IAM_FOLDER --user="$user" --password="$pwd" http://www.fki.inf.unibe.ch/DBs/iamDB/data/ascii/ascii.tgz

tar zxf $IAM_FOLDER/ascii.tgz -C $IAM_FOLDER/ascii
tar zxf $IAM_FOLDER/words.tgz -C $IAM_FOLDER/words