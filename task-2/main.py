#!/usr/bin/env python

import time
import json
import pandas as pd
from datasketch import HyperLogLog

# Function for loading IP addresses from a log file
def load_ip_addresses(filename: str):
    ip_addresses = []
    with open(filename, 'r') as file:
        for line in file:
            try:
                log_entry = json.loads(line)
                ip = log_entry.get("remote_addr")
                if ip:
                    ip_addresses.append(ip)
            except json.JSONDecodeError:
                continue  # Ignore invalid strings
    return ip_addresses

# Accurate counting of unique IP addresses
def exact_count(ips: list) -> int:
    return len(set(ips))

# Counting unique IP addresses with HyperLogLog
def hyperloglog_count(ips: list, precision: int = 10) -> int:
    hll = HyperLogLog(p=precision)
    for ip in ips:
        hll.update(ip.encode('utf-8'))
    return int(hll.count())

# Function for measuring execution time
def measure_time(func, *args):
    start_time = time.time()
    result = func(*args)
    elapsed_time = time.time() - start_time
    return result, elapsed_time

if __name__ == "__main__":
    # Loading data
    filename = "lms-stage-access.log"
    ip_addresses = load_ip_addresses(filename)
    
    # Accurate counting
    exact_result, exact_time = measure_time(exact_count, ip_addresses)
    
    # HyperLogLog counting
    hll_result, hll_time = measure_time(hyperloglog_count, ip_addresses)
    
    # Displaying the results in a table
    data = {
        "Method": ["Accurate counting", "HyperLogLog"],
        "Unique elements": [exact_result, hll_result],
        "Execution time, sec.": [exact_time, hll_time]
    }
    df = pd.DataFrame(data)
    print(f"Results of the comparison:")
    print(df.to_string(index=False))
