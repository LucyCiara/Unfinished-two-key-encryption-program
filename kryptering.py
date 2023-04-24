import sys
import io
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
run = True
FileDataListBinary = []
SboxInfo = open("S-box", "r").readlines()
SboxIn = []
SboxOut = []
outPutList = []
encrypted = []
for item in SboxInfo:
    SboxIn.append(item[:8])
    SboxOut.append(item[9:-1])

print("This program requires you to:")
print("1. Have already run keyCreation")
print("2. Gotten someone else's public key file")
print("3. Renamed it public_key_share.pem")
print("4. Moved the public key file to the folder this program is located in")
print("Continue? y/n")
while run == True:
    yesno = input()
    if yesno == "y":
        #!  ------CODE FROM https://nitratine.net/blog/post/asymmetric-encryption-and-decryption-in-python/------
        with open("private_key.pem", "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )
        with open("public_key_share.pem", "rb") as key_file:
            public_key_share = serialization.load_pem_public_key(
                key_file.read(),
                backend=default_backend()
            )
        #!  ------CODE FROM https://nitratine.net/blog/post/asymmetric-encryption-and-decryption-in-python/------
        print("Do you want to encrypt a file, or decrypt a file? e/d")
        encryptdecrypt = input()
        if encryptdecrypt == "e":
            print("Write name of file you want to encrypt:")
            INPUT_FILE = input()
            def get_binary_data(data):
                with open(data, 'rb') as f:
                    binary_data = f.read()
                    return binary_data
            my_data = get_binary_data(INPUT_FILE)
            my_data = list(my_data)
            while len(my_data)%176!=0:
            #   Makes the file divisible by 16
                my_data.append(42)
            #   Makes a list called FileDataListBinary for the binary version of the items in my_data
            #   S-boxes the binary data in FileDataListBinary
            for item in my_data:
                FileDataListBinary.append('{0:08b}'.format(item))
                FileDataListBinary[-1] = SboxOut[SboxIn.index(FileDataListBinary[-1])]
            #*  ------THIS PART WOULD BE REPEATED MULTIPLE TIMES------
            #   Shuffles the binary data in FileDataListBinary
            tempList = []
            for i in range(0, len(FileDataListBinary), 16):
                for x in range(0, 16, 2):
                    tempList.append(FileDataListBinary[i+x])
                for y in range(1, 16, 2):
                    tempList.append(FileDataListBinary[i+y])
            #   Converts binary string to number to turn into bytes again later, and adds them to a more permanent list
            for item in tempList:
                item = int(item, 2)
                outPutList.append(item)

            outPutList = bytes(outPutList)
            print(outPutList[:1])
            #!  ------CODE FROM https://nitratine.net/blog/post/asymmetric-encryption-and-decryption-in-python/------

            for i in range(int(len(outPutList)/176)):
                encrypted.append(public_key_share.encrypt(
                    outPutList[i*176:(i+1)*176],
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                ))
                #   Library doesn't let you encrypt with private key
                # encrypted.append(private_key.encrypt(
                #     outPutList[i*176:(i+1)*176],
                #     padding.OAEP(
                #         mgf=padding.MGF1(algorithm=hashes.SHA256()),
                #         algorithm=hashes.SHA256(),
                #         label=None
                #     )
                # ))

            #!  ------CODE FROM https://nitratine.net/blog/post/asymmetric-encryption-and-decryption-in-python/------
            #*  ------THIS PART WOULD BE REPEATED MULTIPLE TIMES------
            # decrypted = private_key.decrypt(
            #     encrypted,
            #     padding.OAEP(
            #         mgf=padding.MGF1(algorithm=hashes.SHA256()),
            #         algorithm=hashes.SHA256(),
            #         label=None
            #     )
            # )
            with open("Encrypted file", "wb") as f:
                for item in encrypted:
                    f.write(item)
            run = False
        else:
            print("This program is unfinished.")
    elif yesno == "n":
        run = False