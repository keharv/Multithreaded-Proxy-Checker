#Written by keharv 03/24/2022
#read in proxies.txt and checks them
#working proxies are saved to working_proxies.txt
#used for checking HTTP proxies

import requests
import concurrent.futures
global working_proxies
global use_https
#read in proxies.txt
def read_proxies():
    with open("proxies.txt", "r") as f:
        proxies = f.readlines()
    return proxies

def check_proxy(proxy):
    proxy = proxy.strip()
    proxies = {
        "http": "http://" + proxy,
        "https": "http://" + proxy
    }
    try:
        response = None
        if use_https:
            response = requests.get("https://httpbin.org/ip", proxies=proxies, timeout=5)
        else:
            response = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=5)
        if response.status_code == 200:
            print("[+] Valid proxy:", proxy)
            working_proxies.append(proxy)
    except:
        print("[-] Invalid proxy:", proxy)

#use 5 threads to check proxies
def main():
    num_workers = 5 #number of threads
    while(True):
        use_https = input("Require https? (y/n): ")
        if use_https == "y":
            use_https = True
            break
        elif use_https == "n":
            use_https = False
            break
        else:
            print("Invalid input.")
    while(True):
        num_workers = input("Number of threads: ")
        try:
            num_workers = int(num_workers)
            break
        except:
            print("Invalid input.")
    proxies = read_proxies()
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        executor.map(check_proxy, proxies)
    print("[+] Working proxies:", working_proxies)

if __name__ == "__main__":
    working_proxies = []
    main()
    #write working proxies to working_proxies.txt
    with open("working_proxies.txt", "w") as f:
        for proxy in working_proxies:
            f.write(proxy + "\n")
