import socket
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_ip_addresses(domains):
    ip_addresses = {}
    for domain in domains:
        try:
            ip = socket.gethostbyname(domain)
            ip_addresses[domain] = ip
            logging.info(f"Resolved {domain} to {ip}")
        except socket.gaierror:
            ip_addresses[domain] = 'Error: Domain not found'
            logging.error(f"Failed to resolve {domain}")
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
                        logging.info(f"Read existing host: {domain} -> {ip}")
    except FileNotFoundError:
        logging.warning(f"{file_path} not found, will create a new one.")
    return hosts

def write_to_hosts(ip_addresses, file_path='hosts'):
    current_lines = []
    try:
        with open(file_path, 'r') as file:
            current_lines = file.readlines()
    except FileNotFoundError:
        logging.warning(f"{file_path} not found, will create a new one.")

    with open(file_path, 'w') as file:
        # Retain existing lines that aren't being updated
        for line in current_lines:
            if line.strip() and not line.startswith('#'):
                parts = re.split(r'\s+', line.strip())
                if len(parts) >= 2:
                    ip, domain = parts[0], parts[1]
                    if domain not in ip_addresses:
                        file.write(line)
                        logging.info(f"Retained line: {line.strip()}")

        for domain, ip in ip_addresses.items():
            if "Error" not in ip:
                file.write(f"{ip}\t{domain}\n")
                logging.info(f"Updated {domain} -> {ip}")
            else:
                logging.error(f"Skipping {domain} due to error: {ip}")

def read_domains(file_path='domains.txt'):
    domains = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                domain = line.strip()
                if domain:
                    domains.append(domain)
                    logging.info(f"Read domain: {domain}")
    except FileNotFoundError:
        logging.error(f"{file_path} not found.")
    return domains

def main():
    logging.info("Starting script execution.")
    
    domains_file = 'domains.txt'
    hosts_file = 'hosts'

    new_domains = read_domains(domains_file)
    if not new_domains:
        logging.error("No domains to process. Exiting.")
        return

    existing_hosts = read_existing_hosts(hosts_file)
    new_ip_addresses = get_ip_addresses(new_domains)
    
    # Merge new IP addresses with existing ones
    existing_hosts.update(new_ip_addresses)

    write_to_hosts(existing_hosts, hosts_file)

    logging.info("Hosts file has been updated.")
    logging.info("Script execution completed.")

if __name__ == '__main__':
    main()