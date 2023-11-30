from lastpass import Vault, LastPassIncorrectGoogleAuthenticatorCodeError


def get_serverlist(user, pwd):
    "connect to LastPass and pull in servers"
    serverlist = []

    try:
        # First try without a multifactor password
        vault = Vault.open_remote(user, pwd, None, "db-user-audit")
    except LastPassIncorrectGoogleAuthenticatorCodeError as e:
        print(e)
        multifactor_password = input('Enter Authenticator code: ')

        # And now retry with the code
        vault = Vault.open_remote(user, pwd, multifactor_password, "db-user-audit")

    for index, i in enumerate(vault.accounts):
        iname = i.name.decode("utf-8")
        iuser = i.username.decode("utf-8")
        iurl = i.url.decode("utf-8")
        print(iname, iuser, iurl)
        serverlist.append(i)

    return serverlist
