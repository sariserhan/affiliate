#!/bin/bash
echo "app is running.."
streamlit run --server.headless true --server.fileWatcherType none --browser.gatherUsageStats false app.py

# echo "run docker container"
# docker run -d -p 8080:8080 aibestgoods:app
