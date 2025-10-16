#!/bin/bash
# This script prevents Vercel from running default build commands
# The Python app is built by @vercel/python builder in vercel.json
echo "Python Flask app - build handled by @vercel/python"
exit 0
