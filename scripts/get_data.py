
import datetime
import os
import subprocess
import time

from chronos import db
from chronos import models


begin_timestamp = int(time.mktime(datetime.datetime.utcnow().timetuple()))

name = "ServersTest.test_build_update_delete"

os.chdir("/root/openstack-integration-tests/kong")
output = subprocess.check_output(["nosetests", "tests.test_servers:ServersTest.test_build_update_delete"], stderr=subprocess.STDOUT)
duration = output.split("\n")[2].rsplit(" ", 1)[1].split(".")[0]

db_factory = db.Factory('/root/chronos/chronos/chronos.db')
db_cur = db_factory.create()

model = models.Result(begin_timestamp=begin_timestamp, name=name,
                      duration=duration, db=db_cur)
model.save()
