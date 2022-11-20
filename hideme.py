from cryptography.fernet import Fernet

key = b'pT8ZDjwCvnWkfPEYBm12q2p9srNkM-nWC6Ss9aAcMEw='

# key = Fernet.generate_key()
fernet = Fernet(key)


def encPwd(pwd):
    global fernet
    encPwd = fernet.encrypt(pwd.encode())
    return encPwd


def decPwd(pwd):
    global fernet
    decPwd = fernet.decrypt(pwd).decode()
    return decPwd
