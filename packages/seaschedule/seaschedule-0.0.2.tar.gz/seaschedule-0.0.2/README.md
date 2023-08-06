# seaschedule
Get sea schedules from Maersk and other shipping lines.

## Installation
From [PyPI](https://pypi.org/project/seaschedule/):

    python -m pip install seaschedule

## Setup
The following setup must be done before running seaschedule:
1. Create below environment variables in your OS environment:
    * `SS_SMTP_HOST`: SMTP host for sending notification emails
    * `SS_IB_SFTP_USER`: SFTP user for uploading schedule files to Information Broker
    * `SS_IB_SFTP_PWD`: SFTP password for uploading schedule files to Information Broker
    * `SS_MAEU_API_KEY`: API key given by Maersk 
<br/><br/>
2. Specify below directory paths in `site-packages\seaschedule\config\config.toml` for storing the schedule data files and log files. For example:
    ```
    [environment]
    directory.data = "/home/user1/seaschedule/data"
    directory.log = "/home/user1/seaschedule/log"

    # Windows
    directory.data = "C:\Users\user1\Documents\seaschedule\data"
    directory.log = "C:\Users\user1\Documents\seaschedule\data"
    ```

## How to Use
seaschedule is a console application, named `seaschedule`.

    >>> python -m seaschedule
