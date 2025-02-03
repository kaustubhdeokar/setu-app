#!/bin/bash
sleep 5
NGROK_URL=$(curl --silent http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url')
echo "NGROK_URL=${NGROK_URL}" > /ngrok.env
echo "ngrok URL is: ${NGROK_URL}"