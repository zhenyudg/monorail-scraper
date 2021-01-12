# Monorail Scraper

This project is under active development.

Monorail Scraper is a tool to scrape and retrieve data from 
[Monorail](https://bugs.chromium.org/), an 
issue tracking tool.

Monorail Scraper includes a tool specifically for scraping 
ClusterFuzz-generated OSS-Fuzz issues.

## Prerequisites

Google Chrome needs to be installed, and `chromedriver` needs to be in `PATH`.
Get `chromedriver` here: https://chromedriver.chromium.org/downloads

## Usage

`scrape_one_issue.py` scrapes one single issue from any Monorail project.

Usage: `python3 scrape_one_issue.py [-h] -p PROJECT -i ISSUE_ID`

e.g.: `python3 scrape_one_issue.py -p oss-fuzz -i 20000`

----------------------------------------------------------------------

`scrape_oss_fuzz_issue_range.py` scrapes a continuous range of OSS-Fuzz issues.

Usage: `python3 scrape_oss_fuzz_issue_range.py [-h] -s START -e END`

e.g.: `python3 scrape_oss_fuzz_issue_range.py -s 10000 -e 20000`

----------------------------------------------------------------------

`scrape_previous_errors.py` attempts to rescrape what a past attempt failed at scraping
(based on the error messages of the past attempt).

Usage: `python3 scrape_previous_errors.py [-h] [--rescrape_perm_denied_errs] err_report_path`

e.g.: `python3 scrape_previous_errors.py --rescrape_perm_denied_errs ../scraper_stderr_output.err`
