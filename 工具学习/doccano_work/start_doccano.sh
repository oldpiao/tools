source activate py38
doccano webserver --port 8001 >> logs/doccano_server.log 2>&1 &
doccano task >> logs/doccano_task.log 2>&1 &

