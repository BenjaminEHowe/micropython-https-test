import gc
import urequests

# the below files must be saved on the microcontroller
import common


# format: hostname (str), should connect (bool or None)
HOSTS = (
    ("https://expired.badssl.com/", False),
    ("https://wrong.host.badssl.com/", False),
    ("https://self-signed.badssl.com/", False),
    ("https://untrusted-root.badssl.com/", False),
    ("https://rc4.badssl.com/", False),
    ("https://rc4-md5.badssl.com/", False),
    ("https://dh480.badssl.com/", False),
    ("https://dh512.badssl.com/", False),
    ("https://dh1024.badssl.com/", False),
    ("https://null.badssl.com/", False),
    ("https://tls-v1-0.badssl.com:1010/", False),
    ("https://tls-v1-1.badssl.com:1011/", False),
    ("https://cbc.badssl.com/", False),
    ("https://3des.badssl.com/", False),
    ("https://revoked.badssl.com/", False),
    ("https://pinning-test.badssl.com/", False),
    ("https://no-sct.badssl.com/", False),
    ("https://1000-sans.badssl.com/", None),
    ("https://10000-sans.badssl.com/", None),
    ("https://sha384.badssl.com/", None),
    ("https://sha512.badssl.com/", None),
    ("https://rsa8192.badssl.com/", None),
    ("https://no-subject.badssl.com/", None),
    ("https://no-common-name.badssl.com/", None),
    ("https://incomplete-chain.badssl.com/", None),
    ("https://tls-v1-2.badssl.com:1012/", True),
    ("https://sha256.badssl.com/", True),
    ("https://rsa2048.badssl.com/", True),
    ("https://ecc256.badssl.com/", True),
    ("https://ecc384.badssl.com/", True),
    ("https://mozilla-modern.badssl.com/", True),
)


if __name__ == "__main__":
    common.setup_board()
    for host in HOSTS:
        print("Connecting to {}...".format(host[0]), end=" ")
        try:
            response = urequests.get(host[0])
            print("connected", end=" ")
            if (host[1]) == False:
                print("FAIL")
            else:
                print("PASS")
        except OSError as e:
            print("OSError", end=" ")
            if (host[1]) == True:
                print("FAIL")
            else:
                print("PASS")
            print(e)
        finally:
            response.close()
        gc.collect()
