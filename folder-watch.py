import inotify.adapters

i = inotify.adapters.InotifyTree('/home/pointftp/SIM1')

for event in i.event_gen():
    print(event)