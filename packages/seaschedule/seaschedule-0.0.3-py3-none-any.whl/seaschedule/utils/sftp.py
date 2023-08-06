import paramiko

from pathlib import Path


def put_files(host: str, port: int, username: str, password: str, files: list, remote_directory: str) -> None:
    with paramiko.SSHClient() as ssh:
        # ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port=port, username=username, password=password)
        sftp = ssh.open_sftp()
        for file in files:
            sftp.put(file, remote_directory + "/" + Path(file).name)
