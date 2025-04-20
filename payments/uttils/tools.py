import uuid
import time
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pss
from base64 import b64decode, b64encode
from ..config.config import ENV_VARIABLES

def sign(request):
    privateKey = ENV_VARIABLES["privateKey"]
    exclude_fields = ["sign", "sign_type", "header", "refund_info", "openType", "raw_request"]
    join=[]
    for key in request:
        if key in exclude_fields:
            continue
        if key == "biz_content":
            biz_content = request["biz_content"]
            for k in biz_content:
                join.append(k+"="+biz_content[k])
        else:
            join.append(key+"="+request[key])
    join.sort()
    separator = '&'
    inputString = str(separator.join(join))
    return SignWithRSA(inputString,privateKey,"SHA256withRSA")
# """ Generate signature
#       :param data: the key=value&key2=value2 format signature source string
#       :param key: Sign key
#       :param sign_type: sign type SHA256withRSA or HmacSHA256
#       :return: sign string
# """
def SignWithRSA(data,key, sign_type="SHA256withRSA"):
    if sign_type == "SHA256withRSA":
        key_bytes = b64decode(key.encode("utf-8"))
        key = RSA.importKey(key_bytes)
        digest = SHA256.new()
        digest.update(data.encode("utf-8"))
        signer = pss.new(key)
        signature = signer.sign(digest)
        return b64encode(signature).decode("utf-8")
    else:
        return "Only allowed to the type SHA256withRSA hash"

#  * @Purpose: Creating a new merchantOrderId
#  *
#  * @Param: no parameters
#  * @Return: returns a string format of time (UTC)
def createMerchantOrderId():
    return str(int(time.time()))

def createTimeStamp():
    return str(int(time.time()))

def createNonceStr():
    return str(uuid.uuid1())