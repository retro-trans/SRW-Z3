"""Hold RPCS3's one fragile GDB connection open and relay packets to scripts.

RPCS3's GDB server (config `GDB Server: 127.0.0.1:2345`) dies the moment a
client disconnects, and it is only created on the first boot of a session
(the game's post-install exitspawn restarts emulation without it -- launch
with the install cache in place). So one process connects once and stays
connected; experiments talk to this bridge instead.

Bridge protocol on 127.0.0.1:2346, line based, many requests per connection:
    client sends   <payload>\n      (a GDB packet payload, no $ or #cs)
    bridge replies <reply payload>\n
RPCS3 answers every command with a packet (an empty one for `c`), so every
request gets exactly one reply; a later stop reply is fetched with `!recv`.
`!quit` stops the bridge.

Breakpoints need the PPU interpreter (the LLVM recompiler never traps), so
with the default config this is a memory read/write channel: `m`, `M`, `p`.

    python tools/gdbbridge.py [rpcs3_host:port] [bridge_port]
"""
import socket
import sys
import threading


class Rsp:
    def __init__(self, host, port):
        self.s = socket.create_connection((host, port), timeout=None)
        self.lock = threading.Lock()
        self.s.settimeout(60)

    @staticmethod
    def _frame(payload):
        cs = sum(payload.encode("latin-1")) & 0xFF
        return ("$%s#%02x" % (payload, cs)).encode("latin-1")

    def _recv_packet(self):
        data = b""
        while True:
            c = self.s.recv(1)
            if not c:
                raise ConnectionError("rpcs3 closed the connection")
            if c == b"+":
                continue
            if c == b"$":
                data = b""
                while True:
                    c = self.s.recv(1)
                    if c == b"#":
                        self.s.recv(2)
                        self.s.sendall(b"+")
                        return data.decode("latin-1")
                    data += c

    def call(self, payload):
        with self.lock:
            if payload == "!recv":
                self.s.settimeout(5)
                try:
                    return self._recv_packet()
                except socket.timeout:
                    return "!timeout"
                finally:
                    self.s.settimeout(60)
            if payload == "!int":              # GDB interrupt: a bare 0x03, answered by a stop reply
                self.s.sendall(bytes((3,)))
                self.s.settimeout(10)
                try:
                    return self._recv_packet()
                except socket.timeout:
                    return "!timeout"
                finally:
                    self.s.settimeout(60)
            self.s.sendall(self._frame(payload))
            return self._recv_packet()


def serve(rsp, port):
    srv = socket.socket()
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", port))
    srv.listen(5)
    print("bridge listening on 127.0.0.1:%d" % port, flush=True)
    NL = bytes((10,))
    while True:
        c, _ = srv.accept()
        buf = b""
        try:
            while True:
                while NL not in buf:
                    chunk = c.recv(1 << 20)
                    if not chunk:
                        raise ConnectionError
                    buf += chunk
                line, buf = buf.split(NL, 1)
                payload = line.decode("latin-1")
                if payload == "!quit":
                    c.sendall(b"bye" + NL)
                    return
                try:
                    reply = rsp.call(payload)
                except Exception as e:      # noqa: BLE001
                    reply = "!error %s" % e
                c.sendall(reply.encode("latin-1") + NL)
        except (ConnectionError, OSError):
            pass
        finally:
            c.close()


def main(argv):
    host, port = (argv[1] if len(argv) > 1 else "127.0.0.1:2345").split(":")
    bport = int(argv[2]) if len(argv) > 2 else 2346
    rsp = Rsp(host, int(port))
    print("connected to rpcs3 gdb; qSupported -> %s" % rsp.call("qSupported")[:80], flush=True)
    serve(rsp, bport)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
