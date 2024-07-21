import socket
import re

def get_ip_addresses(domains):
    ip_addresses = {}
    for domain in domains:
        try:
            ip = socket.gethostbyname(domain)
            ip_addresses[domain] = ip
        except socket.gaierror:
            ip_addresses[domain] = 'Error: Domain not found'
    return ip_addresses

def read_existing_hosts(file_path='hosts'):
    hosts = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.strip() and not line.startswith('#'):
                    parts = re.split(r'\s+', line.strip())
                    if len(parts) >= 2:
                        ip, domain = parts[0], parts[1]
                        hosts[domain] = ip
    except FileNotFoundError:
        pass
    return hosts

def write_to_hosts(ip_addresses, file_path='hosts'):
    current_lines = []
    try:
        with open(file_path, 'r') as file:
            current_lines = file.readlines()
    except FileNotFoundError:
        pass

    with open(file_path, 'w') as file:
        # Retain existing lines that aren't being updated
        for line in current_lines:
            if line.strip() and not line.startswith('#'):
                parts = re.split(r'\s+', line.strip())
                if len(parts) >= 2:
                    ip, domain = parts[0], parts[1]
                    if domain not in ip_addresses:
                        file.write(line)

        for domain, ip in ip_addresses.items():
            if "Error" not in ip:
                file.write(f"{ip}\t{domain}\n")
            else:
                print(f"Skipping {domain} due to error: {ip}")

def main():
    new_domains = [
        "github.global.ssl.fastly.net",
        "assets-cdn.github.com",
        "documentcloud.github.com",
        "gist.github.com",
        "gist.githubusercontent.com",
        "github.githubassets.com",
        "help.github.com",
        "nodeload.github.com",
        "raw.github.com",
        "status.github.com",
        "training.github.com",
        "avatars.githubusercontent.com",
        "avatars0.githubusercontent.com",
        "avatars1.githubusercontent.com",
        "avatars2.githubusercontent.com",
        "avatars3.githubusercontent.com",
        "avatars4.githubusercontent.com",
        "avatars5.githubusercontent.com",
        "avatars6.githubusercontent.com",
        "avatars7.githubusercontent.com",
        "avatars8.githubusercontent.com",
        "favicons.githubusercontent.com",
        "codeload.github.com",
        "github-cloud.s3.amazonaws.com",
        "github-com.s3.amazonaws.com",
        "github-production-release-asset-2e65be.s3.amazonaws.com",
        "github-production-user-asset-6210df.s3.amazonaws.com",
        "github-production-repository-file-5c1aeb.s3.amazonaws.com",
        "githubstatus.com",
        "github.community",
        "media.githubusercontent.com",
        "camo.githubusercontent.com",
        "raw.githubusercontent.com",
        "cloud.githubusercontent.com",
        "user-images.githubusercontent.com",
        "customer-stories-feed.github.com",
        "pages.github.com",
        "api.github.com",
        "live.github.com",
        "githubapp.com",
        "github.dev",
        "github.com",
        "alive.github.com",
        "central.github.com",
        "collector.github.com",
        "desktop.githubusercontent.com",
        "github.blog",
        "github.io",
        "github.map.fastly.net",
        "objects.githubusercontent.com",
        "pipelines.actions.githubusercontent.com",
        "private-user-images.githubusercontent.com",
        "vscode.dev",
        "education.github.com",
        "developer.github.com",
        "enterprise.github.com",
        "docs.github.com",
        "www.githubstatus.com"
    ]

    existing_hosts = read_existing_hosts()
    new_ip_addresses = get_ip_addresses(new_domains)
    
    # Merge new IP addresses with existing ones
    existing_hosts.update(new_ip_addresses)

    write_to_hosts(existing_hosts)

    print("Hosts file has been updated.")

if __name__ == '__main__':
    main()
