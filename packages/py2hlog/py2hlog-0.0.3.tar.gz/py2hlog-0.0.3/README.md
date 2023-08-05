# py2hlog (Python to HTML log)
https://github.com/houshmand-2005/py2hlog

Python logs to HTML formatter

simple useage :
```bash
from py2hlog import logger
obj1 = logger.py2hlog()  # create an object from py2hlog
obj1.file_name = "new_log_file.txt"  # here write the log detail
try:
    if a == 2:
        print("Iam working!")
except:
    obj1.error("I dont have any 'a' variable")
print("print obj1: ", obj1)
time.sleep(5)  # to see time changing
obj1.debug("Add a variable before the 'if' like a = 3")
obj1.makehtml("py2hlog.html")  # enter the name of output file
# you can also use these statuses :
# _____________________________
# obj1.critical("your message")
# obj1.debug("your message")
# obj1.info("your message")
# obj1.warning("your message")
# obj1.error("your message")
# _____________________________

```
You can also see which file the log belongs to and when the log was added.
**THIS IS BETA VERSION**

**https://houshmand-2005.github.io/**
houshmand2005
