# jobsearch
Check for changes on list of urls of career pages (or just pages in general)

## Installation
1. clone and cd into the directory
1. `pip install -r requirements.txt`
1. [Download the appropriate version of Chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)
    1. Unzip and move the chromedriver executable to the jobsearch directory
    1. You might get an error like `Error: “chromedriver” cannot be opened because the developer cannot be verified. Unable to launch the chrome browser`. If so, try [this solution from StackOverflow](https://stackoverflow.com/a/60374958/190902).

## Configuration
1. Update the list of urls in the `urls.txt` file. One url per line.

## Running
1. From the command line, just run `python -m jobs`
1. The script will output the results. It might takes a while depending how many urls and what else your comptuer is doing.
It takes my slow machine about 30 seconds to run about 15 sites.

## Notes
Both `jobs.json` and `urls.txt` are committed with empty / default settings, and then ignored from further commits. If you want to do that on your local branch, run:

    git update-index --skip-worktree urls.txt jobs.json

To undo and start tracking again:

    git update-index --no-skip-worktree urls.txt jobs.json
    
To see what files are being skipped:

    git ls-files -v . | grep ^S

_[Source](https://stackoverflow.com/a/39776107/190902)_
