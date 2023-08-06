import subprocess
import requests
import json

def get_cpu_id():
    ret = subprocess.run(['fastboot', 'oem', 'get_device_id'], capture_output=True)
    cpu_id = ret.stderr.decode('ascii').split('\n')[0].split('(bootloader) ')[1].strip()
    return cpu_id

def auth_start():
    # step 1, get nonce by run 'fastboot oem f_auth_start'
    ret = subprocess.run(['fastboot', 'oem', 'f_auth_start'], capture_output=True)
    nonce = ret.stderr.decode('ascii').split('\n')[3].split('(bootloader) ')[1]
    print(f"Success to get nonce from the phone: {nonce} \n")
    return nonce

def sign(nonce):
    # step 2, get auth response from auth server
    cpuid = get_cpu_id()
    print(f"cpu_id = {cpuid}\n")

    print("Waiting for sign from anth server...")
    header = {"Content-Type": "application/json"}
    payload = {"project": "sunfire", "cpuid": cpuid, "nonce": nonce}
    ret = requests.post("http://192.168.12.81:8888/no_auth/AuthDownload/", headers = header, data = json.dumps(payload))
    auth_resp = json.loads(ret.content.decode('ascii'))['nonce']
    print(f"Success to get the signature: {auth_resp} \n")
    return auth_resp

def step3(auth_resp):
    # step 3, get auth response to phone to verify, by run 'fastboot oem permission factory xxxxxx
    ret = subprocess.run(['fastboot', 'oem', 'permission', 'factory', auth_resp], capture_output=True)
    print(f"Authorise result: \n {ret.stderr.decode('ascii')}")
    return ret

def authorise():
    print("Please go into fastboot mode...")
    nonce = auth_start()         # step 1, get nonce by run 'fastboot oem f_auth_start'
    signed_data = sign(nonce)    # step 2, get auth response from auth server
    step3(signed_data)           # step 3, send auth response to phone to verify, by run 'fastboot oem permission factory xxxxxx

if __name__ == "__main__":
    authorise()
