# ASC PLATFORM CRAWLER

## Introduction

to web crawl the platforms, save the reports in local folder and then upload to the NAS

## Quick Start

### 1. Prerequisite

Install `Python 3.10` or above

### 2. Environment Variables

Create a `.env` file at project root by duplicating the `.env.example`, provide appropriate values for the environment variables. Required credentials can be found on 1Password. 

### 3. Dependencies

Create a virtual environment and install the required packages 

```
> python -m venv .venv

> .venv\Scripts\activate

(.venv) > pip install -r requirements.txt
```
### 4. Platform 
Set up platform specific requirements, including but not limited to the followings. More details can be found in the platform's `README.md`
|Platform|Details|
|-|-|
|abg|Require access to Outlook mail folder **Research ABG**|
|gs|Require access to Outlook mail folder **Research GS**|
|td|Require access to Outlook mail folder **Research TD**|

### 5. Start Crawling

Start the program by running `main.py`

```
> python -m main
```

#### Optional args
|Arg|Details|Values|Default|
|-|-|-|-|
|`-h`, `--help`|Show help message and exit|||
|`-u`, `--upload`|Upload downloaded files to NAS|||
|`-rm`, `--remove`|Remove downloaded files|||
|`-v`, `--verbosity`|Different level of debug messages|1, 2, 3|1|

```
> python -m main -u -rm -v 2
```