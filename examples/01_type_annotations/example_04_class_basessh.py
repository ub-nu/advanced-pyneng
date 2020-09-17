import paramiko
import time
from typing import Union, List, Iterable


class BaseSSH:
    def __init__(self, ip: str, username: str, password: str) -> None:
        self.ip = ip
        self.username = username
        self.password = password
        self._MAX_READ = 10000

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(
            hostname=ip,
            username=username,
            password=password,
            look_for_keys=False,
            allow_agent=False,
        )

        self._ssh = client.invoke_shell()
        time.sleep(1)
        self._ssh.recv(self._MAX_READ)

    def close(self) -> None:
        self._ssh.close()

    def send_show_command(self, command: str) -> str:
        self._ssh.send(command + "\n")
        time.sleep(2)
        result = self._ssh.recv(self._MAX_READ).decode("ascii")
        return result

    def send_config_commands(self, commands: Union[str, Iterable[str]]) -> str:
        if isinstance(commands, str):
            commands = [commands]
        for command in commands:
            self._ssh.send(command + "\n")
            time.sleep(0.5)
        result = self._ssh.recv(self._MAX_READ).decode("ascii")
        return result


if __name__ == "__main__":
    r1 = BaseSSH("192.168.100.1", "cisco", "cisco")
    print(r1.send_show_command("sh ip int br"))
    print(r1.send_show_command("enable"))
    print(r1.send_show_command("cisco"))
    print(
        r1.send_config_commands(
            ("conf t", "int loopback 33", "ip address 3.3.3.3 255.255.255.255", "end")
        )
    )
