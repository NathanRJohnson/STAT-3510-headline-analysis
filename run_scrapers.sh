#!/bin/bash
echo "NYT"
python3 scrapers/new_york_times.py

echo "WSJ"
python3 scrapers/wall_street_journal.py

echo "WP"
python3 scrapers/washington_post.py

echo "WT"
python3 scrapers/washington_times.py

echo "Performing Sentiment Analysis"
python3 sentiment.py 