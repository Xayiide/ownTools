import subprocess, socket, time, struct
# from _winreg import *
def recv_data(sock):
    data_len = struct.unpack("!I", sock.recv(4))
    return sock.recv(data_len)

def send_data(sock, data):
    data_len = len(data)
    sock.send(struct.pack("!I", data_len))
    sock.send(data)
    return

def create_user(name, pwd, log_file):
    cmd_list = ["net",
                "user",
                "/add",
                name,
                pwd]
    subprocess.Popen(cmd_list, 0, None, None, log_file, log_file)
    log_file.close()
    f = open("log.txt", "r")
    data = f.read()
    f.close()
    return data

def delete_user(name, log_file):
    cmd_list = ["net",
                "user",
                "/del",
                name]
    subprocess.Popen(cmd_list, 0, None, None, log_file, log_file)
    log_file.close()
    f = open("log.txt", "r")
    data = f.read()
    f.close()
    return data

def download_registry_key(root, path, sock):
    key_hdl = CreateKey(root, path)
    num_subkeys, num_Values, l_modified = QueryInfoKey(key_hdl)
    print "Numkeys: %d\nValues: %d\n" %(num_subkeys, num_Values)
    for i in range(num_subkeys):
        print EnumKey(key_hdl, i)
    for i in range(num_Values):
        v_name, v_data, d_type = EnumValue(key_hdl, i)
        print "%s : %d" %(v_name, v_data)
    return
