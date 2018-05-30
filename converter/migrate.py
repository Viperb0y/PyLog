old_logs = list(filter(lambda x: True if x!="\n" else False,open("to_convert","r").readlines()))
new_logs = []
DATE = ""
TIME = ""
TYPE = ""
CONTENT = ""
entry_types = {"***":"Dream","~~~":"Editable","###":"Spooky Coincidence","^^^":"Quote","@@@":"Image Link"}
entry_types_set = set(["***","~~~","###","^^^","@@@"])
for line in old_logs:
    if "[[" in line and "]]" in line and len(line) < 20:
        date = line[2:-2].split(".")
        for i in range(len(date)):
            if len(date[i]) == 1:
                date[i] = "0"+date[i]
        DATE = ".".join(date)
    if "(" in line and ")" in line and ":" in line and len(line) < 10:
        if "M" in line:
            print(line)
        time = line[1:-1].split(":")
        for i in range(len(time)):
            if len(time[i] == 1):
                time[i] = "0"+time[i]
        TIME = ":".join(time)
    if line[:3] in entry_types_set:
        TYPE = entry_types[line[:3]]
        CONTENT = line[3:]

#THIS IS GONNA WORK.
