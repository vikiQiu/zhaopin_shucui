#!/bin/mysql
use zhaopin;

load data infile "/data/github/zhaopin_shucui/qiancheng/data/qiancheng$year/\[qiancheng\]DataAnalysis$today.csv"
into table qiancheng
FIELDS TERMINATED BY ',' ENCLOSED BY '"';

load data infile "/data/github/zhaopin_shucui/qiancheng/data/qiancheng$year/\[qiancheng\]DataMining$today.csv"
into table qiancheng
FIELDS TERMINATED BY ',' ENCLOSED BY '"';
