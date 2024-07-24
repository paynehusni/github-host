# GitHub Hosts Updater

This project aims to solve issues related to GitHub domain name pollution by automatically updating the `hosts` file with the correct IP addresses for GitHub domains. 

GitHub RAW: [hosts](https://raw.githubusercontent.com/paynehusni/github-host/master/hosts) <br>
jsDelivr CDN: [hosts](https://cdn.jsdelivr.net/gh/paynehusni/github-host/hosts)

## Features

- **Hosts File Update**: Updates the `hosts` file to include the correct IP addresses for these domains.
- **Automation with GitHub Actions**: Includes a GitHub Actions workflow to automate the process, ensuring the `hosts` file is updated regularly without manual intervention.

## Hosts File Path

### Windows
```
C:\Windows\System32\drivers\etc\hosts
```
We recommend using the [open-source tool](https://github.com/paynehusni/github-host/releases/tag/1.0) from our project to update the hosts file on Windows.
### Linux
```
/etc/hosts
```
### macOS
```
/etc/hosts
```