#!/usr/bin/env bash
hadoop fs -rm -r xiyouji-output
hadoop jar  /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.8.2.jar \
  -files ./mapper.py,./reducer.py,./jieba.mod,./idf.txt \
  -mapper "python3 ./mapper.py" \
  -reducer "python3 ./reducer.py" \
  -input xiyouji/* -output xiyouji-output