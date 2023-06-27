echo "正在停止doccano server, port: 8001..."
lsof -i:8001 | awk '{print $2}' | xargs kill -9 >/dev/null 2>&1
lsof -i:8001

echo "正在停止doccano task"
ps -ef|grep "doccano task" | awk '{print $2}' | xargs kill -9 >/dev/null 2>&1
ps -ef|grep "doccano task"

