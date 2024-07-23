import socket
import re
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_ip_addresses(domains):
    ip_addresses = {}
    for domain in domains:
        try:
            ip = socket.gethostbyname(domain)
            ip_addresses[domain] = ip
            logging.info(f"Resolved {domain} to {ip}")
        except socket.gaierror as e:
            ip_addresses[domain] = 'Error: Domain not found'
            logging.error(f"Failed to resolve {domain}: {e}")
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
    except IOError as e:
        logging.error(f"Error reading {file_path}: {e}")
    return hosts

def write_to_hosts(ip_addresses, file_path="hosts"):
    current_lines = []
    try:
        with open(file_path, "r") as file:
            current_lines = file.readlines()
    except FileNotFoundError:
        logging.warning(f"{file_path} not found, will create a new one.")
    except IOError as e:
        logging.error(f"Error reading {file_path}: {e}")

    try:
        with open(file_path, "w") as file:
            # Write header comments
            file.write("# github-hosts start\n")

            # Retain existing lines that aren't being updated
            for line in current_lines:
                if line.strip() and not line.startswith("#"):
                    parts = re.split(r"\s+", line.strip())
                    if len(parts) >= 2:
                        ip, domain = parts[0], parts[1]
                        if domain not in ip_addresses:
                            file.write(line)
                            logging.info(f"Retained line: {line.strip()}")

            for domain, ip in ip_addresses.items():
                if "Error" not in ip:
                    # Ensure IP address is formatted to align
                    formatted_ip = ip.ljust(15)  # Adjust the number based on your needs
                    file.write(f"{formatted_ip}\t{domain}\n")
                    logging.info(f"Updated {domain} -> {formatted_ip}")
                else:
                    logging.error(f"Skipping {domain} due to error: {ip}")

            # Write footer comments
            current_time = datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")
            file.write(f"# {current_time}\n")
            file.write("# https://github.com/paynehusni/github-host\n")
            file.write("# github-hosts end\n")
    except IOError as e:
        logging.error(f"Error writing to {file_path}: {e}")

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
    except IOError as e:
        logging.error(f"Error reading {file_path}: {e}")
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
