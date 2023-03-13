from licensing.models import *
from licensing.methods import Key, Helpers

RSAPubKey = "<RSAKeyValue><Modulus>vD0LrQaKZa0eyV30YQJUikvUlTQsgKAjylMUO/aH5fA+7d30Yn66ziqrRxAzLStQ4MPvUDVltJr+szOq9V5B6otlotzJpDbIhq9hjqsOZsgJ4D9nsJz5NC92/oRKHEBQIbOJVInFWkAnHI4DACg/At23MUIakGMe56WiSXUYJ6faXHAt30/3+zet6akwmdg+zrs1PfNtD/Qv5ck9KcCCBdFToQtFK1282mLgZMBO9mGTt8TNk+T/1Ti9XvuGpA7KCf/pjJ9eYs/zCQuB0CkCMmUr8P6xUGbjqScEMPNdFh3Yz6pKDKlIVC4I2AFSlXHyYF5GeT5cCAZnDgDSlgncZw==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"
auth = "WyI0MDk2NzQwMiIsIjdTMHhNbWhYcDR5c2QrY0pJeWxHNGMxNVVreGpHeHJUdTFmQWVzTGQiXQ=="

result = Key.activate(token=auth,\
                   rsa_pub_key=RSAPubKey,\
                   product_id=19239, \
                   key="LLKPQ-ZGGWH-EZUHO-RNNBJ",\
                   machine_code=Helpers.GetMachineCode(v=2))

if result[0] == None or not Helpers.IsOnRightMachine(result[0], v=2):
    # an error occurred or the key is invalid or it cannot be activated
    # (eg. the limit of activated devices was achieved)
    print("The license does not work: {0}".format(result[1]))
else:
    # everything went fine if we are here!
    print("The license is valid!")
    license_key = result[0]
    print("Feature 1: " + str(license_key.f1))
    print("License expires: " + str(license_key.expires))