old_logs = list(filter(lambda x: True if x!="\n" else False,open("to_convert","r").readlines()))
new_logs = []
got_date = False
pack = []
for i in range(old_logs.index("[[3.9.2016.]]\n"),len(old_logs)):
    if "[[" in old_logs[i]:
        print(old_logs[i])
        if got_date:
            print(old_logs[i])
            new_logs.append(pack[:])
            del pack[:]
            got_date = False
            pack.append(old_logs[i][2:-3])
        else:
            got_date = True
            pack.append(old_logs[i][2:-3])
    else:
        pack.append(old_logs[i])
to_write = []
print(new_logs[1])
#KINDA WORKS BUT NOT QUITE
entry_types = {"***":"Dream","~~~":"Editable","###":"Spooky Coincidence","^^^":"Quote","@@@":"Image Link"}
for i in new_logs[2:]:
    date = i[0]
    time = "undef"
    entry_type = "undef"
    for j in i[1:]:
        if "(" in j and len(j) < 20 and any([c.isdigit() for c in j]):
            time=j[1:-2].replace(" ","")
            pass
            if "AM" in time:
                time=time.replace("AM","")
            if "PM" in time:
                t=time.replace("PM","").split(":")
                hrs = t[0] if t[0][0] != "0" else t[0][1:]
                hrs = "".join(i for i in hrs if i.isdigit())
                time=str(int(hrs)+12)+":"
                if len(t) == 2:
                    time+=t[1]
                else:
                    time+="00"
        to_break = False
        if j[:3] in entry_types:
            to_write.append("{}\t{}\t{}\t{}".format(date,time,entry_types[j[:3]],j[3:]))
            to_break = True
        else:
            to_write.append("{}\t{}\t{}\t{}".format(date,time,entry_type,j))
f = open("out","w")
f.write("".join(to_write))
f.close()
#new_logs = [[]]
#for i in range(49,len(old_logs)):
#    if "[[" in old_logs[i] and "2" in old_logs[i]:
#        new_logs.append([old_logs[i][2:-3]+"\t"])
#    elif ":" in old_logs[i] and len(old_logs[i]) < 20:
#        new_logs[-1].append(old_logs[i][1:-2]+"\t")
#    elif len(old_logs[i]) > 15:
#        if len(new_logs[-1]) == 2:
#            new_logs[-1].append(old_logs[i])
#        elif len(new_logs[-1]) == 3:
#            new_logs[-1][-1]+=old_logs[i]
#    else:
#        print(old_logs[i-1][:-1])
##print(new_logs[1])
