#!/bin/bash

PORT=5000
#python_flask_command=nohup python3 main.py > flask_output.log 2>&1 &"
FLASK_APP_COMMAND="nohup python3 main.py > flask_output.log 2>&1 &"

PID=$(lsof -ti:$PORT)

if [ -n "$PID" ]; then

	echo "Flask app running on port $PORT with PID $PID. Terminating..."
	kill -9 $PID
else

	echo "NO process running on port $PORT"

fi

echo "Restarting Flask app"

echo "Evaluating python command: $FLASK_APP_COMMAND"
#eval $python_flask_command
eval $FLASK_APP_COMMAND
sleep 2

NEWPID=$(lsof -ti:$PORT)

if [ -n "$NEWPID" ]; then

	echo "App running with PID $NEWPID"
else

	echo "Failed to restart the app"
fi
