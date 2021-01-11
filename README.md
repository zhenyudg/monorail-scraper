# Monorail Scraper

This project is under active development.

Monorail Scraper is a tool to scrape and retrieve data from 
[Monorail](https://bugs.chromium.org/), an 
issue tracking tool.

Monorail Scraper includes a tool specifically for scraping 
ClusterFuzz-generated OSS-Fuzz issues.

## Usage

`scrape_one_issue.py` scrapes one single issue from any Monorail project.

`scrape_oss_fuzz_issue_range.py` scrapes a continuous range of OSS-Fuzz issues.

`scrape_previous_errors.py` attempts to rescrape what a past attempt failed at scraping
(based on the error messages of the past attempt).
