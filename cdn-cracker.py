import requests
import concurrent.futures
import time
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Extract command line arguments
if len(sys.argv) < 4 or sys.argv[1] == '-h' or sys.argv[1] == '--help':
    print("Usage: python fin4.py [target_title] [file_path] [domain]")
    print("Arguments:")
    print("  target_title   - The target HTML title to search for")
    print("  file_path      - The file path to save the results")
    print("  domain         - The domain name to modify the Host header")
    sys.exit()

target_title = sys.argv[1]
file_path = sys.argv[2]
domain = sys.argv[3]

# Modify the Host header to the domain name
headers = {'Host': domain}

def check_ip(ip_address):
    file = open(file_path, "a")
    http_url = f"http://{ip_address}"
    https_url = f"https://{ip_address}"                                                                                              

    try:                                                                                                                                        
        http_response = requests.get(http_url, headers=headers, timeout=10, verify=False)                                                           

        # Check if the HTTP response was successful
        if http_response.status_code == 200:                                                                                                                           
            # Get the HTML content                                                                                                                                     
            http_html_content = http_response.text                                                                                                                     

            # Check if the HTML title contains the specified value                                                                                                                             
            if target_title in http_html_content:                                                                                                                                              
                file.write(f"IP address {ip_address} (HTTP) belongs to domain {domain}\n")
    except requests.exceptions.RequestException as e:                                                                                                                                                                          
        pass                                                                                                                                                                                                                   

    try:                                                                                                                                                                                                                       
        https_response = requests.get(https_url, headers=headers, timeout=10, verify=False)                                                                                                                                    

        # Check if the HTTP response was successful                                                                                                                                                                            
        if https_response.status_code == 200:                                                                                                                                                                                  
            # Get the HTML content                                                                                                                                                                                                                                         
            https_html_content = https_response.text                                                                                                                                                                                                                       

            # Check if the HTML title contains the specified value                                                                                                                                                                                                         
            if target_title in https_html_content:                                                                                                                                                                                                                         
                file.write(f"IP address {ip_address} (HTTPS) belongs to domain {domain}\n")                                                                                                                                                                                                                                                   
    except requests.exceptions.RequestException as e:                                                                                                                                                                                                                                                                                         
        pass                                                                                                                                                                                                                                                                                                                                  
                                                                                                                                                                                                                                                                                                                                              
# Read IP addresses from a file                                                                                                                                                                                                                                                                                                               
with open('ips.txt', 'r') as file:                                                                                                                                                                                                                                                                                                        
    ip_addresses = file.read().splitlines()                                                                                                                                                                                                                                                                                                                                                                                                                   

total_ips = len(ip_addresses)                                                                                                                                                                                                                                                                                                                                                                                                                                 

start_time = time.time()                                                                                                                                                                                                                                                                                                                                                                                                                                      

# Specify the number of threads for concurrent execution                                                                                                                                                                                                                                                                                                                                                                                                      
num_threads = 100                                                                                                                                                                                                                                                                                                                                                                                                                                             

# Check IP addresses concurrently using ThreadPoolExecutor
with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:                                                                                                                                                                                                                                                                                                                                                                              
    futures = [executor.submit(check_ip, ip_address) for ip_address in ip_addresses]                                                                                                                                                                                                                                                                                                                                                                          

    for completed_ips, _ in enumerate(concurrent.futures.as_completed(futures), start=1):
        progress = completed_ips / total_ips
        elapsed_time = time.time() - start_time
        remaining_time = (elapsed_time / progress) - elapsed_time
        percentage = int(progress * 100)
        elapsed_hours, elapsed_remainder = divmod(elapsed_time, 3600)
        elapsed_minutes, elapsed_seconds = divmod(elapsed_remainder, 60)
        remaining_hours, remaining_remainder = divmod(remaining_time, 3600)
        remaining_minutes, remaining_seconds = divmod(remaining_remainder, 60)
        print(f"\rProgress: {percentage}% ({completed_ips}/{total_ips}), Elapsed Time: {int(elapsed_hours):02d}:{int(elapsed_minutes):02d}:{int(elapsed_seconds):02d}, Remaining Time: {int(remaining_hours):02d}:{int(remaining_minutes):02d}:{int(remaining_seconds):02d}", end='')                                                                                                                                                                         

# Print completion message                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
print("\nAll IP addresses checked.") 
