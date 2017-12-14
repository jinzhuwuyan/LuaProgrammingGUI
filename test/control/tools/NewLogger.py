import colorstreamhandler
import logging
import logging.config
class InitLog():
    def __init__(self):
        
        _LOGCONFIG = {
                "version": 1,
                "disable_existing_loggers": False,

                "handlers": {
                    "console": {
                        "class": "colorstreamhandler.ColorStreamHandler",
                        "stream": "ext://sys.stderr",
                        "level": "INFO"
                    }
                },

                "root": {
                    "level": "INFO",
                    "handlers": ["console"]
                }
            }

        logging.config.dictConfig(_LOGCONFIG)


    def getLogger(self):

        return logging.getLogger("mylogger")
        
if __name__ == '__main__':
    log = InitLog()
    mylogger = log.getLogger()
    mylogger.warning("foobar")
    mylogger.info("info foobar")
    mylogger.error("error foobar")