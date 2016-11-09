from mender.cli import device
import random
import time
import os

"""
    Uses a the backend-mender-cli tool to create a fake, updateable device.

    - Specify the device_type by setting the env. variable. ex: DEVICE="beaglebone" ..
    - If you'd rather want some custom inventory data, set the env. variable INVENTORY
    - If you want to the update to fail, set the variable FAIL, the value will be used in the fail log message
"""

class Args(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__


# The mender-backend-cli is expecting CLI arguments, the following sets the required arguments.
args = Args()
args.device_key = "key"
args.service = os.environ.get("GATEWAY", "https://docker.mender.io")
args.mac_address = ":".join(["%02x" % random.randint(0x00, 0xFF) for i in range(6)])
args.verify = False
args.tenant_token = "dummy"
args.seq_no = 1
args.device_token = "devtoken"

if os.environ.get("DEVICE", False):
    args.attrs_set = ["device_type:%s" % (os.environ["DEVICE"]), "image_id:fake-dummy-client"]
elif os.environ.get("INVENTORY", False):
    args.attrs_set = os.environ["INVENTORY"].split(",")
else:
    raise Exception("Neither DEVICE or INVENTORY env. variable were set")

args.wait = 45
args.fail = os.environ.get("FAIL", False)


# Generate key
device.do_key(args)
device.do_authorize(args)

# Loop until the device is authorized
count = 2
while True:
    time.sleep(2)
    args.seq_no = count
    if device.do_authorize(args):
        break
    else:
        count += 1

# Set inventory values, and wait for update
device.do_inventory(args)
device.do_fake_update(args)
