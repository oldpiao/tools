echo "检查端口服务是否启动：doccano webserver --port 8001"
lsof -i:8001
echo "检查task是否启动：doccano task"
ps -ef|grep "doccano task"

