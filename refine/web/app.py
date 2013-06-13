#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os, subprocess
import shutil
import re
import time
import flask, os, sys, time, psutil, json, socket
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.wsgi import WSGIContainer

from flask import Flask, render_template, g, redirect, request, url_for
from ujson import loads
from subprocess import *
from functools import wraps
from flask import request, Response
from werkzeug import secure_filename
from refine.version import __version__
from refine.app.utils import flush_dead_mappers
from refine.app.keys import MAPPERS_KEY, JOB_STATUS_KEY, JOB_TYPES_KEY, JOB_TYPE_KEY, LAST_PING_KEY, MAPPER_ERROR_KEY, MAPPER_WORKING_KEY, JOB_TYPES_ERRORS_KEY, ALL_KEYS, PROCESSED, PROCESSED_FAILED, CURRENT_EDIT, CURRENT_CONTENT, CURRENT_RESULT, JOB_TEST, ELASTIC_ENDPOINT

ALLOWED_EXTENSIONS = set(['tar', 'py'])
app = Flask(__name__)

def job_desc(type):
    f = open(app.config['UPLOAD_FOLDER'] + type + "/app_config.py")
    desc = ""
    for line in f.readlines():
        line = str(line.strip('\n'))
        if line.startswith("#Desc"):
            desc = line[5:]
            break
    return desc

def update_desc(type, desc):
    filename = app.config['UPLOAD_FOLDER'] + type + "/app_config.py"
    f = open(filename)
    lines = f.readlines()
    newlines = []
    have_desc = 0
    for line in lines:
        if line.startswith("#Desc"):
            newlines.append("#Desc" + desc + "\n")
            have_desc = 1
        else:
            newlines.append(line)
    if have_desc == 0:
        newlines.insert(2, "#Desc" + desc + "\n")
    f.close()
    f = open(filename, "w")
    for line in newlines:
        f.write(line)
    f.close()

def job_schedule(type):
    f = open("/var/spool/cron/crontabs/root")
    res = ""
    for line in f.readlines():
        line = str(line.strip('\n'))
        if (type.encode("ascii") in line):
          lines = line.split(" ")
          res = lines[0] + " " + lines[1] + " " + lines[2] + " " + lines[3] + " " + lines[4]
    f.close()
    return res


def remove_schedule(type):
    f = open("/var/spool/cron/crontabs/root")
    lines = f.readlines()
    newLines = []
    for line in lines:
        if (type.encode("ascii") in line):
            continue
        else:
            newLines.append(line)
    f.close()
    f = open("/var/spool/cron/crontabs/root", "w")
    for line in newLines:
        f.write(line)
    f.close()
    call(["service", "cron", "restart"])

def new_schedule(type, schedule):
    f = open("/var/spool/cron/crontabs/root", "r")
    lines = f.readlines()
    f.close()
    f = open("/var/spool/cron/crontabs/root", "w")
    port = job_port(type)
    newline = schedule.encode("ascii").strip() + " " + "curl -XGET " + "'" + "http://" + app.config['WEB_HOST'] + ":" + str(port) + "/stream/" + type.encode("ascii") + "'" + " >> /var/log/" + type.encode("ascii") + ".log"
    for line in lines:
        f.write(line)
    if "\n" in lines[-1]:
        f.write(newline + "\n")
    else:
        f.write("\n" + newline + "\n")
    f.close()
    call(["service", "cron", "restart"])

def job_port(type):
    f = open("port.config")
    res = '9999'
    for line in f.readlines():
        line = line.strip('\n')
        key = line.split("=")[0]
        val = line.split("=")[1]
        if (key == type):
          res = val
    f.close()
    return res


def remove_port(type):
    f = open("port.config")
    lines = f.readlines()
    newLines = []
    for line in lines:
        key = line.split("=")[0]
        val = line.split("=")[1]
        if (key == type):
            continue
        else:
            newLines.append(line)
    f.close()
    f = open("port.config", "w")
    for line in newLines:
        f.write(line)
    f.close()

def new_port(type):
    f = open("port.config", "r")
    lines = f.readlines()
    lastline = lines[-1].strip('\n')
    val = int(lastline.split("=")[1])
    val = val + 1
    f.close()
    f = open("port.config", "w")
    for line in lines:
        f.write(line)
    if "\n" in lines[-1]:
        f.write(type.encode("ascii")+ "=" + str(val))
    else:
        f.write("\n" + type.encode("ascii")+ "=" + str(val))
    f.close()


def allowed_file(filename):
    return '.' in filename and \
       filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def server_context():
    return {
        'surfikiMR_service_status': 'running',
        'surfikiMR_version': __version__
    }

@app.before_request
def before_request():
    g.config = app.config
    g.server = server_context()
    g.job_types = app.db.connection.smembers(JOB_TYPES_KEY)
    g.jobsdef = get_all_jobs_def()
    g.jobstreams = get_alll_job_streams()
    g.jobschedules = get_all_job_schedules()
    g.jobs = get_all_jobs(g.job_types)
    g.jobstatus = get_all_status(g.job_types)
    g.jobsdesc = get_all_job_descs()
    g.jobhint = get_all_hints(g.job_types)
    g.jobtesthints = get_all_test_hints(g.job_types)
    g.mappers = get_mappers()
    g.currentfile = get_current_file()
    g.currentcontent = get_current_file_content()
    g.currenttestresult = ""
    g.jobtestlinks = get_all_test_link(g.job_types)

def get_all_test_link(alljobs):
    all_test_links = {}
    for job in alljobs:
       if app.db.connection.sismember(JOB_TEST, job):
           all_test_links[job] = "http://" + app.config['WEB_HOST'] + ':' + str(app.config['WEB_PORT']) + '/test/' + job
       else:
           all_test_links[job] = ''
    return all_test_links

def get_all_test_hints(job_types):
    all_hints = {}
    for job in job_types:
        if app.db.connection.sismember(JOB_TEST, job):
            all_hints[job] = 'Must click the Enable Test button to get the latest results'
        else:
            all_hints[job] = ''
    return all_hints

def get_all_hints(job_types):
    all_hints = {}
    for job_type in job_types:
        status = app.db.connection.get(JOB_STATUS_KEY % job_type)
        if status != 'INACTIVE':
            all_hints[job_type] = '- Click the Job Result Link to start the Job (Results will display in browser tab created when complete)'
    return all_hints

def get_current_file():
    return app.db.connection.get(CURRENT_EDIT)

def get_current_file_content():
    return app.db.connection.get(CURRENT_CONTENT)

def get_all_status(job_types):
    all_status = {}
    for job_type in job_types:
        status = app.db.connection.get(JOB_STATUS_KEY % job_type)
        all_status[job_type] = status
    return all_status

def get_alll_job_streams():
    all_streams = {}
    for jobdef in g.jobsdef:
        status = app.db.connection.get(JOB_STATUS_KEY % jobdef)
        if status == 'INACTIVE':
            all_streams[jobdef] = ""
        elif status == 'IDLE':
            all_streams[jobdef] = "http://" + app.config['WEB_HOST'] + ':' + job_port(jobdef) + "/stream/" + jobdef + "?last=1"
        else:
            all_streams[jobdef] = "http://" + app.config['WEB_HOST'] + ':' + job_port(jobdef) + "/stream/" + jobdef
    return all_streams

def get_all_job_schedules():
    all_schedules = {}
    for jobdef in g.jobsdef:
        all_schedules[jobdef] = job_schedule(jobdef)
    return all_schedules

def get_all_job_descs():
    all_descs = {}
    for jobdef in g.jobsdef:
        all_descs[jobdef] = job_desc(jobdef)
    return all_descs

def get_mappers():
    all_mappers = app.db.connection.smembers(MAPPERS_KEY)
    mappers_status = {}
    for mapper in all_mappers:
        key = MAPPER_WORKING_KEY % mapper
        working = app.db.connection.lrange(key, 0, -1)
        if not working:
            mappers_status[mapper] = None
        else:
            mappers_status[mapper] = loads(working[0])

    return mappers_status


def get_all_jobs_def():
    all_file_names = {}
    for job_type in os.listdir(app.config['UPLOAD_FOLDER']):
        if job_type != 'template':
	    all_file_names[job_type] = []
	    for name in os.listdir(app.config['UPLOAD_FOLDER'] + '/' + job_type):
	        if name != ('__init__.py') and not name.endswith('pyc'):
                    all_file_names[job_type].append(job_type + "/" + name)
    return all_file_names

def get_all_jobs(all_job_types):
    all_jobs = {}
    for job_type in all_job_types:
        job_type_jobs = app.db.connection.smembers(JOB_TYPE_KEY % job_type)
        all_jobs[job_type] = []
        if job_type_jobs:
            all_jobs[job_type] = job_type_jobs

    return all_jobs

def remove_all_jobs(job_type):
    job_type_jobs = app.db.connection.smembers(JOB_TYPE_KEY % job_type)
    for job_type_job in job_type_jobs:
        app.db.connection.srem(JOB_TYPE_KEY % job_type, job_type_job)
    app.db.connection.delete(JOB_STATUS_KEY % job_type)

def get_errors():
    errors = []
    for job_type in g.job_types:
        errors = [loads(item) for key, item in app.db.connection.hgetall(MAPPER_ERROR_KEY % job_type).iteritems()]

    return errors

@app.route("/")
def index():
    error_queues = app.db.connection.keys(JOB_TYPES_ERRORS_KEY)

    has_errors = False
    for queue in error_queues:
        if app.db.connection.hlen(queue) > 0:
            has_errors = True

    flush_dead_mappers(app.db.connection, MAPPERS_KEY, LAST_PING_KEY)

    key_names = app.db.connection.keys(ALL_KEYS)

    keys = []
    for key in key_names:
        key_type = app.db.connection.type(key)

        if key_type == 'list':
            size = app.db.connection.llen(key)
        elif key_type == 'set':
            size = app.db.connection.scard(key)
        else:
            size = 1

        keys.append({
            'name': key,
            'size': size,
            'type': key_type
        })

    return render_template('index.html', failed_warning=has_errors, keys=keys, info=app.db.connection.info(), endpoint=app.db.connection.get(ELASTIC_ENDPOINT))

@app.route('/ace', methods=['GET', 'POST'])
def ace():
    if request.method == 'POST':
        filename = request.form['filename']
        content = request.form['content']
        writefile = open(app.config['UPLOAD_FOLDER'] + '/' + filename, "w")
        writefile.write(content)
        writefile.close()
        if 'mapper' in filename:
            jobtype = filename.split('_')[1]
            makeTestFile(jobtype)
        return redirect(url_for('start'))
    return render_template('ace.html')

def duplicateJob(old, new):
    if os.path.exists(app.config['UPLOAD_FOLDER'] + new):
        return
    new_port(new)
    call(["mkdir", app.config['UPLOAD_FOLDER'] + new])
    #call(["cp", "-r", ddapp.config['UPLOAD_FOLDER'] + old + "/*", app.config['UPLOAD_FOLDER'] + new])
    subprocess.call("cp -r " + app.config['UPLOAD_FOLDER'] + old + "/* " + app.config['UPLOAD_FOLDER'] + new, shell=True)
    call(["mv", app.config['UPLOAD_FOLDER'] + new + "/" + "test_" + old + ".py", app.config['UPLOAD_FOLDER'] + new + "/" + "test_" + new + ".py"])
    call(["mv", app.config['UPLOAD_FOLDER'] + new + "/" + "surfiki_" + old + "_stream.py", app.config['UPLOAD_FOLDER'] + new + "/" + "surfiki_" + new + "_stream.py"])
    call(["mv", app.config['UPLOAD_FOLDER'] + new + "/" + "surfiki_" + old + "_mapper.py", app.config['UPLOAD_FOLDER'] + new + "/" + "surfiki_" + new + "_mapper.py"])
    call(["mv", app.config['UPLOAD_FOLDER'] + new + "/" + "surfiki_" + old + "_reducer.py", app.config['UPLOAD_FOLDER'] + new + "/" + "surfiki_" + new + "_reducer.py"])

    app.db.connection.sadd(JOB_TYPES_KEY, new)
    app.db.connection.set(JOB_STATUS_KEY % new, "INACTIVE")
    config = app.config['UPLOAD_FOLDER'] + new + "/" + "app_config.py"
    template = open(config).read()
    template = template.replace(old, new)
    makeFile(config, template)

    mapper = app.config['UPLOAD_FOLDER'] + new + "/" + "surfiki_" + new + "_mapper.py"
    template = open(mapper).read()
    template = template.replace(old, new)
    makeFile(mapper, template)

    stream = app.config['UPLOAD_FOLDER'] + new + "/" + "surfiki_" + new + "_stream.py"
    template = open(stream).read()
    template = template.replace(old, new)
    makeFile(stream, template)

    reducer = app.config['UPLOAD_FOLDER'] + new + "/" + "surfiki_" + new + "_reducer.py"
    template = open(reducer).read()
    template = template.replace(old, new)
    makeFile(reducer, template)

def makeFile(filename, filecontent):
    file = open(filename, 'w')
    file.write(filecontent)
    file.close()

def makeNormalFile(jobtype, name):
    filename = os.path.join(app.config['UPLOAD_FOLDER'] + jobtype, name).encode("ascii")
    makeFile(filename, "")

def makeAppConfig(jobtype, desc):
    filename = os.path.join(app.config['UPLOAD_FOLDER'] + jobtype, 'app_config.py').encode("ascii")
    streamdef = jobtype+'.surfiki_' + jobtype + '_stream' + '.Surfiki'+ jobtype + 'Stream'
    reducerdef = jobtype+'.surfiki_' + jobtype + '_reducer' + '.Surfiki'+ jobtype + 'Reducer'
    filecontent = '#!/usr/bin/python\n'+ '# -*- coding: utf-8 -*-\n\n#Desc'+desc+'\n'+'INPUT_STREAMS = [\n    \'' +streamdef+ '\']\n'+'REDUCERS = [\n    \''+reducerdef+'\']'
    makeFile(filename, filecontent)

def makeStream(jobtype):
    filename = os.path.join(app.config['UPLOAD_FOLDER'] + jobtype, 'surfiki_' + jobtype + '_stream.py').encode("ascii")
    template = open(app.config['UPLOAD_FOLDER'] + "template/stream_template.py").read()
    template = template.replace("CLASSNAME", "Surfiki"+ jobtype + "Stream")
    template = template.replace("JOBTYPE", jobtype)
    makeFile(filename, template)

def makeReducer(jobtype):
    filename = os.path.join(app.config['UPLOAD_FOLDER'] + jobtype, 'surfiki_' + jobtype + '_reducer.py').encode("ascii")
    template = open(app.config['UPLOAD_FOLDER'] + "template/reducer_template.py").read()
    template = template.replace("CLASSNAME", 'Surfiki'+ jobtype + 'Reducer')
    template = template.replace("JOBTYPE", jobtype)
    makeFile(filename, template)

def makeMapper(jobtype):
    filename = os.path.join(app.config['UPLOAD_FOLDER'] + jobtype, 'surfiki_' + jobtype + '_mapper.py').encode("ascii")
    template = open(app.config['UPLOAD_FOLDER'] + "template/mapper_template.py").read()
    template = template.replace("CLASSNAME", 'Surfiki'+ jobtype + 'Mapper')
    template = template.replace("JOBTYPE", jobtype)
    makeFile(filename, template)

def makeTestFile(jobtype):
    filename = os.path.join(app.config['UPLOAD_FOLDER'] + jobtype, 'test_' + jobtype + '.py').encode("ascii")
    template = open(app.config['UPLOAD_FOLDER'] + "template/test_template.py").read()
    template = template.replace("JOBTYPE", jobtype)
    mapper_content = open(app.config['UPLOAD_FOLDER'] + jobtype + "/surfiki_" + jobtype + "_mapper.py").read()
    mapper_content = mapper_content[mapper_content.find('def map'):]
    template = template.replace("MAPPER_CONTENT", mapper_content)
    makeFile(filename, template)

def testRunJob(jobtype):
    app.db.connection.sadd(JOB_TEST, jobtype)
    filename  = "/var/log/mrtest/test_" + jobtype + ".log"
    call(["rm", filename])
    call(["touch", filename])
    subprocess.Popen("python " + app.config['UPLOAD_FOLDER'] + jobtype + "/test_" + jobtype + ".py >> " + filename + " 2>&1", shell=True)

def stopJob(job):
    mappers = app.db.connection.smembers(MAPPERS_KEY)
    for mapper in mappers:
        if mapper.startswith(job):
            app.db.connection.delete(LAST_PING_KEY % mapper)
            app.db.connection.srem(MAPPERS_KEY, mapper)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method =='POST':
        if 'Auto Job Type' in request.form:
            auto = request.form['Auto Job Type']
            desc = request.form['Desc']
            if os.path.exists(app.config['UPLOAD_FOLDER'] + auto):
                return render_template('upload.html')
            call(["mkdir", app.config['UPLOAD_FOLDER'] + auto])
            call(["cp", app.config['UPLOAD_FOLDER'] + "template/__init__.py", app.config['UPLOAD_FOLDER'] + auto + "/__init__.py"])
            new_port(auto)
            makeAppConfig(auto, desc)
            makeStream(auto)
            makeReducer(auto)
            makeMapper(auto)
            makeTestFile(auto)
            app.db.connection.sadd(JOB_TYPES_KEY, auto)
            app.db.connection.set(JOB_STATUS_KEY % auto, "INACTIVE")
            return render_template('upload.html')
        jobtype = request.form['Job Type']
        if jobtype.strip() == "":
            return render_template('upload.html')
        call(["rm", "-rf", app.config['UPLOAD_FOLDER'] + request.form['Job Type']])
        call(["mkdir", app.config['UPLOAD_FOLDER'] + request.form['Job Type']])
        call(["cp", app.config['UPLOAD_FOLDER'] + "template/__init__.py", app.config['UPLOAD_FOLDER'] + request.form['Job Type'] + "/__init__.py"])
        remove_port(jobtype)
        new_port(jobtype)
        app.db.connection.sadd(JOB_TYPES_KEY, jobtype)
        app.db.connection.set(JOB_STATUS_KEY % jobtype, "INACTIVE")
        file = request.files['appconfig']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'] + request.form['Job Type'], filename))
        file = request.files['streamfile']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'] + request.form['Job Type'], filename))
        file = request.files['mapperfile']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'] + request.form['Job Type'], filename))
        file = request.files['reducerfile']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'] + request.form['Job Type'], filename))
    return render_template('upload.html')

@app.route("/test/<jobTest>")
def test(jobTest):
    content = open("/var/log/mrtest/test_" + jobTest + ".log").read()
    open("/var/log/mrtest/test_" + jobTest + ".log")
    g.currenttestresult = content
    return render_template('test_job.html')

@app.route('/start', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        if 'Desc' in request.form:
            desc = request.form['Desc']
            job  = request.form['Job Type']
            update_desc(job, desc)
            return redirect("%s%s" % (url_for('index'), "#tab-jobs"))
        if 'New Job' in request.form:
            newjob = request.form['New Job']
            oldjob = request.form['Job Type']
            duplicateJob(oldjob, newjob)
            return redirect("%s%s" % (url_for('index'), "#tab-jobs"))
        if 'New File' in request.form:
            jobnewfile = request.form['Job Type']
            name = request.form['New File']
            makeNormalFile(jobnewfile, name)
            return redirect("%s%s" % (url_for('index'), "#tab-jobs"))
        if 'Filename' in request.form:
            if 'Edit' in request.form:
                app.db.connection.delete(CURRENT_EDIT)
                app.db.connection.set(CURRENT_EDIT, request.form['Filename'])
                return redirect(url_for('ace'))
            else:
                call(["rm", "-rf", app.config['UPLOAD_FOLDER'] + request.form['Filename']])
                return redirect("%s%s" % (url_for('index'), "#tab-jobs"))
        if 'Kill' in request.form:
            jobkill = request.form['Kill']
            # Run kill job scripts to find all the processed related with this job, and kill them
            os.popen('/root/refine/kill_job.sh ' + jobkill)
            stopJob(jobkill)
            app.db.connection.set(JOB_STATUS_KEY % jobkill, "INACTIVE")
            return redirect("%s%s" % (url_for('index'), "#tab-jobs"))
        if 'Test Job' in request.form:
            jobTest = request.form['Test Job']
            testRunJob(jobTest)
            return redirect("%s%s" % (url_for('index'), "#tab-jobs"))
        if 'Delete Job Type' in request.form:
            jobdelete = request.form['Delete Job Type']
            shutil.rmtree(os.path.join(app.config['UPLOAD_FOLDER'] + jobdelete))
            app.db.connection.srem(JOB_TYPES_KEY, jobdelete)
            os.popen('/root/refine/kill_job.sh ' + jobdelete)
            stopJob(jobdelete)
            remove_port(jobdelete)
            remove_all_jobs(jobdelete)
            return redirect("%s%s" % (url_for('index'), "#tab-jobs"))
        if 'Schedule Job' in request.form:
            jobschedule = request.form['Schedule Job']
            scheduleString = request.form['schedule']
            schedule = scheduleString.encode("ascii")
            if len(schedule.strip()) == 0:
                remove_schedule(jobschedule)
            else:
                remove_schedule(jobschedule)
                new_schedule(jobschedule, scheduleString)
            return redirect("%s%s" % (url_for('index'), "#tab-jobs"))
        jobtype = request.form['Job Type']
        counts = "5"
        if 'Mapper' in request.form:
            counts = request.form['Mapper'].encode("ascii")
            if len(counts.strip()) == 0:
                counts = "5"
        filename = None
        classone = None
        classtwo = None
        # before start, kill it first
        os.popen('/root/refine/kill_job.sh ' + jobtype)
        stopJob(jobtype)
        # Traverse all the files under this job, finding the mapper file, and retrieve the mapper class name
        for r,d,f in os.walk(app.config['UPLOAD_FOLDER'] + '/' +jobtype):
            for files in f:
                if files.endswith("_mapper.py"):
                    filename = files
                    for line in open(os.path.join(r,files)):
                        if line.startswith("class"):
                            classtwo = line.split(' ')[1].split('(')[0]
        classone = filename[:-3]
        mapperclass = classone+"."+classtwo
        # Start the App in backgorund process
        subprocess.Popen('python refine/app/server.py --redis-port='+ str(app.config['REDIS_PORT']) + ' -p '+ job_port(jobtype) + ' --redis-pass=surfikiMR --config-file=jobs/refine/' + jobtype + '/app_config.py', shell=True,stdout=PIPE)
        # Start all the mappers in background process
        for num in range(1, int(counts)+1):
            subprocess.Popen('python refine/worker/mapper.py --mapper-key=map-key-'+jobtype+str(num) + ' --mapper-class='+jobtype+'.'+mapperclass+' --redis-port='+ str(app.config['REDIS_PORT']) + ' --redis-pass=surfikiMR', shell=True,stdout=PIPE)
        app.db.connection.set(JOB_STATUS_KEY % jobtype, "READY")
        return redirect("%s%s" % (url_for('index'), "#tab-jobs"))
    return render_template('run_job.html')

@app.route('/raw')
def raw():
	diskused = 0
	disktotal = 0
	for i in psutil.disk_partitions():
		try:
			x = psutil.disk_usage(i.mountpoint)
			diskused += x.used
			disktotal += x.total
		except OSError:
			pass
	o = json.dumps({
		'uptime':	time.time() - psutil.BOOT_TIME,
		'fqdn':		"Refine",
		'cpuusage':	psutil.cpu_percent(0),
		'ramusage':	psutil.virtual_memory(),
		'diskio':	psutil.disk_io_counters(),
		'diskusage':	[diskused, disktotal],
		'netio':	psutil.network_io_counters(),
		'swapusage':	psutil.swap_memory()
	})
	return flask.Response(o, mimetype='application/json')

@app.route("/mappers")
def mappers():
    flush_dead_mappers(app.db.connection, MAPPERS_KEY, LAST_PING_KEY)
    return render_template('mappers.html')

@app.route("/failed")
def failed():
    return render_template('failed.html', errors=get_errors())

@app.route("/failed/delete")
def delete_all_failed():
    for job_type in g.job_types:
        key = MAPPER_ERROR_KEY % job_type
        app.db.connection.delete(key)

    return redirect(url_for('failed'))

@app.route("/failed/delete/<job_id>")
def delete_failed(job_id):
    for job_type in g.job_types:
        key = MAPPER_ERROR_KEY % job_type
        if app.db.connection.hexists(key, job_id):
            app.db.connection.hdel(key, job_id)

    return redirect(url_for('failed'))

@app.route("/job-types")
def job_types():
    return render_template('job-types.html')

@app.route('/configuration', methods=['GET', 'POST'])
def configuration():
    if request.method == 'POST':
        app.db.connection.set(ELASTIC_ENDPOINT, request.form['endpoint'])
        return redirect("%s%s" % (url_for('index'), "#tab-configuration"))
    else:
        return render_template('configuration.html', info=app.db.connection.info(), endpoint=app.db.connection.get(ELASTIC_ENDPOINT))

@app.route('/paramedic.js', methods=['GET'])
def paramedic():
    return render_template('paramedic.js', endpoint=app.db.connection.get(ELASTIC_ENDPOINT))

@app.route('/sense', methods=['GET'])
def sense():
    return render_template('sense.html', endpoint=app.db.connection.get(ELASTIC_ENDPOINT))

@app.route("/stats")
def stats():
    info = app.db.connection.info()
    key_names = app.db.connection.keys(ALL_KEYS)

    keys = []
    for key in key_names:
        key_type = app.db.connection.type(key)

        if key_type == 'list':
            size = app.db.connection.llen(key)
        elif key_type == 'set':
            size = app.db.connection.scard(key)
        else:
            size = 1

        keys.append({
            'name': key,
            'size': size,
            'type': key_type
        })

    processed = app.db.connection.get(PROCESSED)
    processed_failed = app.db.connection.get(PROCESSED_FAILED)

    return render_template('stats.html', info=info, keys=keys, processed=processed, failed=processed_failed, errors=get_errors())

@app.route("/stats/keys/<key>")
def key(key):
    key_type = app.db.connection.type(key)

    if key_type == 'list':
        value = app.db.connection.lrange(key, 0, -1)
        multi = True
    elif key_type == 'set':
        value = app.db.connection.smembers(key)
        multi = True
    else:
        value = app.db.connection.get(key)
        multi = False

    return render_template('show_key.html', key=key, multi=multi, value=value)

@app.route("/stats/keys/<key>/delete")
def delete_key(key):
    app.db.connection.delete(key)
    return redirect(url_for('stats'))


