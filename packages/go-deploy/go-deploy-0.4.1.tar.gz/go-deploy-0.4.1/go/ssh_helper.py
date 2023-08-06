import paramiko


def parse_public_key(public_key_path):
    import paramiko
    from pathlib import Path

    path = Path(public_key_path).expanduser().absolute()
    return paramiko.PublicBlob.from_file(path)


def parse_private_key(private_key_path):
    import paramiko
    from pathlib import Path

    path = Path(private_key_path).expanduser().absolute()

    try:
        return paramiko.RSAKey.from_private_key_file(path)
    except Exception:
        return paramiko.ecdsakey.ECDSAKey.from_private_key_file(path)

class SshHelper:
    def __init__(self, host, user, key_path, port=22):
        self.host = host
        self.user = user
        self.key = parse_private_key(key_path)
        self.client = None
        self.port = port


    def connect(self, timeout=10):
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.host, username=self.user, pkey=self.key, port=self.port, timeout=timeout)

    # noinspection PyBroadException
    def close_quietly(self):
        if self.client:
            try:
                self.client.close_quietly()
                self.client = None
            except Exception:
                pass
