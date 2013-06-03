import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

if __name__ == "__main__":
    class RefineEventHandler(FileSystemEventHandler):
        def onChangeMapper(self, jobtype):
            upload_foloder = '/surfiki-refine-elasticsearch/jobs/refine/'
            filename = os.path.join(upload_foloder + jobtype, 'test_' + jobtype + '.py').encode("ascii")
            template = open(upload_foloder + "template/test_template.py").read()
            template = template.replace("JOBTYPE", jobtype)
            mapper_content = open(upload_foloder + jobtype + "/surfiki_" + jobtype + "_mapper.py").read()
            mapper_content = mapper_content[mapper_content.find('def map'):]
            template = template.replace("MAPPER_CONTENT", mapper_content)
            file = open(filename, 'w')
            file.write(template)
            file.close()

        def on_created(self, event):
            print "on_created:: " + event.src_path 
        def on_moved(self, event):
            print "on_moved:: " + event.src_path + "  " + event.dest_path
        def on_deleted(self, event):
            print "on_deleted:: " + event.src_path
        def on_modified(self, event):
            path = event.src_path
            if path.endswith("mapper.py"):
                print "Modified Mapper Code: " + path
                dels = path.split('/')
                job = dels[len(dels) - 1].split('_')[1]
                self.onChangeMapper(job)
    event_handler = RefineEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path='/surfiki-refine-elasticsearch/jobs/refine/', recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
