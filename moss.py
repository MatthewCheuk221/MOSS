import socket
import sys
import os

languages = [
    "c", "cc", "java", "ml", "pascal", "ada", "lisp", "scheme", "haskell", "fortran",
    "ascii", "vhdl", "perl", "matlab", "python", "mips", "prolog", "spice", "vb",
    "csharp", "modula2", "a8086", "javascript", "plsql", "verilog"
]

server = "moss.stanford.edu"
port = 7690
noreq = "Request not sent."
usage = "usage: moss.py [-x] [-l language] [-d] [-b basefile1] ... [-b basefilen] [-m #] [-c \"string\"] file1 file2 file3 ..."

userid = "your_userid"

# Default options
opt_l = "c"
opt_m = 10
opt_d = 0
opt_x = 0
opt_c = ""
opt_n = 250
opt_b = []

# Parse options
argv = sys.argv[1:]
i = 0
while i < len(argv) and argv[i].startswith("-"):
    flag = argv[i][1]
    rest = argv[i][2:] if len(argv[i]) > 2 else ''
    i += 1
    value = rest or (argv[i] if i < len(argv) else None)

    if flag == "d":
        opt_d = 1
    elif flag == "x":
        opt_x = 1
    elif flag == "b":
        if not value:
            sys.exit("No argument for option -b.\n")
        opt_b.append(value)
        if not rest:
            i += 1
    elif flag == "l":
        if not value:
            sys.exit("No argument for option -l.\n")
        opt_l = value
        if not rest:
            i += 1
    elif flag == "m":
        if not value:
            sys.exit("No argument for option -m.\n")
        opt_m = int(value)
        if not rest:
            i += 1
    elif flag == "c":
        if not value:
            sys.exit("No argument for option -c.\n")
        opt_c = value
        if not rest:
            i += 1
    elif flag == "n":
        if not value:
            sys.exit("No argument for option -n.\n")
        opt_n = int(value)
        if not rest:
            i += 1
    elif flag == "s":
        server = argv[i]
        i += 1
    elif flag == "p":
        port = int(argv[i])
        i += 1
    else:
        sys.exit(f"Unrecognized option -{flag}. {usage}\n")

# Remaining args are input files
input_files = argv[i:]
if not input_files:
    sys.exit(f"No files submitted.\n{usage}")

# File checks
print("Checking files . . .")
for f in opt_b + input_files:
    if not os.path.exists(f):
        sys.exit(f"File {f} does not exist. {noreq}\n")
    if not os.access(f, os.R_OK):
        sys.exit(f"File {f} is not readable. {noreq}\n")
    try:
        with open(f, 'r') as test:
            test.read(1)
    except Exception:
        sys.exit(f"File {f} is not a text file. {noreq}\n")
print("OK")

# Connect to server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((server, port))
except Exception as e:
    sys.exit(f"Could not connect to server {server}: {e}\n")

def send(msg):
    sock.sendall(msg.encode('utf-8'))

def recv_line():
    return sock.recv(1024).decode('utf-8').strip()

def upload_file(filename, file_id, language):
    try:
        size = os.path.getsize(filename)
        print(f"Uploading {filename} ...", end='', flush=True)
        with open(filename, 'r') as f:
            content = f.read()
        sanitized_name = filename.replace(' ', '_')
        send(f"file {file_id} {language} {size} {sanitized_name}\n")
        send(content)
        print("done.")
    except Exception as e:
        sys.exit(f"Error uploading file {filename}: {e}")

# Protocol handshake
send(f"moss {userid}\n")
send(f"directory {opt_d}\n")
send(f"X {opt_x}\n")
send(f"maxmatches {opt_m}\n")
send(f"show {opt_n}\n")
send(f"language {opt_l}\n")

msg = recv_line()
if msg == "no":
    send("end\n")
    sys.exit(f"Unrecognized language {opt_l}.")

# Upload base files
for base in opt_b:
    upload_file(base, 0, opt_l)

# Upload submission files
for idx, f in enumerate(input_files, start=1):
    upload_file(f, idx, opt_l)

# Submit query
send(f"query 0 {opt_c}\n")
print("Query submitted. Waiting for the server's response.\n")
print(recv_line())
send("end\n")
sock.close()
