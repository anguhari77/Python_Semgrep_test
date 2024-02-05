# semgrep-testing
## How is it work?
Semgrep scanning run at github-baymax-org-level-webhook, receives event from SQS on every pull-merge_request from PRs. 
It will create semgrep issues at github issue section with the label `security-issue`, it would ignore if the issue is already created or if it is closed as a False Positive.

## Developer side/action
Checking the issues, if they are FPs (False Positives), please add the label `FP` and a comment why it is a False Positive but do not close the issue since this will be reviewed by **product security** team (we will run a cron job once a week to get FPs open to review), once it is confirmed as FP, the issue can be closed.
If the issue was fixed, please add a comment explain it and close the issue without `FP` label.