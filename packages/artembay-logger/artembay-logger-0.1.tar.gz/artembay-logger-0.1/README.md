# Just another logger for python

This logger has been writen by Artem Bay. Can used in any project

main.py:
```py
from logger import Logger

if __name__ == "__main__":
    logger = Logger(log_file="log.txt", log_level=3, log_timezone="Europe/Moscow", log_colors=True)
    logger.info(f"All log levels will writen in file but print only selectd and lower Now log level is {logger.log_level} \n")
    logger.debug("Debug [Log level 1]")
    logger.info("Info [Log level 2]")
    logger.warning("Warning [Log level 3]")
    logger.error("Error [Log level 4]")
    logger.critical("Critical [Log level 5]")
```

log.txt:
```
2022-11-03 05:21:52 |INFO    | All log levels will writen in file but print only selectd and lower Now log level is 3 
 
2022-11-03 05:21:52 |DEBUG   | Debug [Log level 1] 
2022-11-03 05:21:52 |INFO    | Info [Log level 2] 
2022-11-03 05:21:52 |WARNING | Warning [Log level 3] 
2022-11-03 05:21:52 |ERROR   | Error [Log level 4] 
2022-11-03 05:21:52 |CRITICAL| Critical [Log level 5] 
```

Dm me in discord for help. Artem Bay#0547

Made with ❤️ by Artem Bay and Github Copilot