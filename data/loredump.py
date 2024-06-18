string_to_file = ""
for line in open("data/loredump.txt", "r").read().splitlines():
    if line.startswith("PT:") is False:
        continue
    else:
        line = line.lstrip("PT:")
        line = line.lstrip()
        string_to_file += "{char}: " + line +"\n"
string_to_file = string_to_file.strip()
with open("data/characterai.txt", "w") as f:
    f.write(string_to_file)