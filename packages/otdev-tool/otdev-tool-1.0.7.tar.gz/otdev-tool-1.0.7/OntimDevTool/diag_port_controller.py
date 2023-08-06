import subprocess
import requests
import json
import base64
import struct

def get_device_id():
    ret = subprocess.run(['fastboot', 'oem', 'get_device_id'], capture_output=True)
    device_id = ret.stderr.decode('ascii').split('\n')[0].split('(bootloader) ')[1].strip()
    print(f"Get device id: {device_id}")
    return device_id

def sign(project, data):
    print("Waiting for sign from anth server...")
    header = {"Content-Type": "application/json"}
    payload = {"project": project, "data": data}
    ret = requests.post("http://192.168.12.81:8888/no_auth/SignDIAG/", headers = header, data = json.dumps(payload))
    sign_resp = json.loads(ret.content.decode('ascii'))['data']
    # print(f"sign diag success, resp = {sign_resp}")
    return sign_resp

def set_diag_port(data):
    if data:
        # open diag
        dia_tmp_file = "diag.bin"
        with open(dia_tmp_file, "w") as tmp_file:
            tmp_file.write(data)

        ret = subprocess.run(['fastboot', 'flash', 'diag', dia_tmp_file], capture_output=True)
        if ret.stderr.decode('ascii').split('\n')[-1].find("Finished. Total time:") != -1:
            return True
        else:
            print(ret.stderr.decode('ascii'))
            return False
    else:
        # close diag
        ret = subprocess.run(['fastboot', 'oem', 'diag_lock'], capture_output=True)
        if ret.stderr.decode('ascii').split('\n')[-1].find("Finished. Total time:") != -1:
            return True
        else:
            print(ret.stderr.decode('ascii'))
            return False


def open_diag_port(project):
    print("Please go into fastboot mode...")
    device_id = get_device_id()
    sigature = sign(project, device_id + "DIAG_ENABLE")
    ret = set_diag_port(sigature)
    if ret:
        print("Success to open the Diag Port.")
    else:
        print("Failed to open the Diag Port.")

def close_diag_port():
    ret = set_diag_port(None)
    if ret:
        print("Success to close the Diag port.")
    else:
        print("Failed to close the Diag Port.")


if __name__ == "__main__":
    open_diag_port("sunfire")
    # close_diag_port()
