# Platforms

This document provides a high level guideline on standardising the platform crawlers.

## Design principles

Each platform should follow the design of abstract class `Crawler` carefully. You are advised to create a `Helper` for each platform, inheriting `Crawler` . To increase readability, methods in `Helper` class should be handling the underlying operations, where the main `Platform` class should only implement the abstract methods. 

Methods in platform `Helper` class can be more specific to the platform's behaviour, while modules in `utils` should be more general to maximise reusability. 

## Upon deploying

### Update requirements.txt

Add new packages to `requirements.txt`, check carefully when merging with other branches. 

### Test with mypy

Run mypy to check with linting and typing, for example

```
> mypy ./src/platforms/{my_platform} ./src/utils
```

Click [here](https://mypy.readthedocs.io/en/stable/command_line.html) for more details