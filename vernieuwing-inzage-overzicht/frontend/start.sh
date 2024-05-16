#! /bin/sh

echo "Start nuxt node server"
node /app/server/index.mjs 

# echo "Start nginx as proxy server"
# nginx -g "daemon off;"

echo "done"
