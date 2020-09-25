import inotify.adapters
#
#i = inotify.adapters.InotifyTree('/home/pointftp/SIM1')
#
#for event in i.event_gen():
#    print(event)


i = inotify.adapters.inotify()

i.add_watch('/home/pointftp/SIM1')

    for event in i.event_gen(yield_nones=False):
        (_, type_names, path, filename) = event

        print("PATH=[{}] FILENAME=[{}] EVENT_TYPES={}".format(
              path, filename, type_names))