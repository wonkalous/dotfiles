import subprocess
import json
import time
import sys
import re


def get_tree():
    j_ = subprocess.check_output(
        ["i3-msg", "-t", "get_tree"]
    ) 
    j = json.loads(j_)
    return j

def get_wins():
    return dict(proc_tree(get_tree()))

def proc_tree(x):
    print(x['type'], len(x["nodes"]))
    if x["type"] == "workspace":
        return sum([proc_workspace(z, x["name"]) for z in x["nodes"]], [])
    else:
        return sum([proc_tree(z) for z in x["nodes"]], [])

def proc_workspace(x, ws):
    if x["window"] is not None:
        return [(x["name"], ws)]
    else:
        return sum([proc_workspace(z, ws) for z in x["nodes"]], [])

def ascii_only(s, r=''):
    out = ''
    skip = False
    for i in range(len(s)):
        if i < len(s)-1 and ord(s[i+1]) >= 128 and s[i] == "\\":
            skip = True
            out += r
            continue
        if skip:
            skip = False
            continue
        if ord(s[i]) >= 128:
            out += r
            continue
        out += s[i]
    return out


def place_wins(wins):
    cmd = "[title=\"{title}\"] move --no-auto-back-and-forth window to workspace number {ws}"
    for t, n in wins.iteritems():
        print(t, ascii_only(t))
        print(re.escape(t))
        print(ascii_only(re.escape(t)))
        cmd_ = cmd.format(title=ascii_only(re.escape(t), r='.'), ws=n)
        print("i3-msg '"+cmd_+"'")

        # raw_input()
        try:
            subprocess.check_output([
                "i3-msg",
                cmd_
            ])
        except Exception as e:# [subprocess.CalledProcessError, UnicodeEncodeError]:
            print("ERROR: ", t, n)
            print(e)

if __name__ == '__main__':
    if sys.argv[1] == 'save':
        wins = get_wins()
        if len(sys.argv) > 2:
            filename = sys.argv[2] 
        else:
            filename = "wins_{}".format(int(time.time()))
        with open(filename, 'w+') as out:
            json.dump(wins, out)
    elif sys.argv[1] == 'load':
        with open(sys.argv[2], 'r') as wins_file:
            wins = json.load(wins_file)
        place_wins(wins)


#"[title=\"1966 - Google Chrome\"] move window to workspace number 13"