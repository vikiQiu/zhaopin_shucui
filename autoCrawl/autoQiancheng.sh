#!/bin/sh

export today=$(date +%Y%m%d)
export year=$(date +%Y%m)
cd /data/github/zhaopin_shucui/qiancheng

scrapy crawl qiancheng -o data/qiancheng$year/[qiancheng]DataMining$today.csv -t csv>>log/log$year/[log]DM$today.txt
scrapy crawl qiancheng2 -o data/qiancheng$year/[qiancheng]DataAnalysis$today.csv -t csv>>log/log$year/[log]DA$today.txt
