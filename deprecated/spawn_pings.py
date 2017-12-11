import pexpect
import signal

SSH_CMD = 'ssh root@192.168.10.101'
PING_CMD = 'ping -I tap0 192.168.200.2 -f &'

terms = []


def main():
    for i in range(50):
        t = pexpect.spawn(SSH_CMD)
        t.sendline(PING_CMD)
        terms.append(t)

if __name__ == "__main__":
    try:
        main()
        print 'PRESS CTRL + C to quit'
        signal.pause()

    except KeyboardInterrupt:
        for t in terms:
            t.sendline('killall ping')
