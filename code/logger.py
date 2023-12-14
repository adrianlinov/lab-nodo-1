import sys
import utime


class Logger:
    def __init__(self, log_file="logfile.txt", activado=True):
        self.log_file = log_file
        self.activado = activado
        # print("LOGGER INICIADO")
        with open(self.log_file, "a") as f:
            f.write("==== INICIO ====\n")
            f.close()

    def log(self, message, level="INFO"):
        try:
            if self.activado == True:
                timestamp = utime.localtime()
                formatted_time = "{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(
                    timestamp[0], timestamp[1], timestamp[2],
                    timestamp[3], timestamp[4], timestamp[5]
                )
                log_entry = "{} [{}] {}\n".format(formatted_time, level, message)
                # print(message)
                with open(self.log_file, "a") as f:
                    f.write(log_entry)
                    f.close()
        except Exception as e:
            print(sys.print_exception(e))


    def logException(self, message, level="ERROR"):
        try:
            if self.activado == True:
                timestamp = utime.localtime()
                formatted_time = "{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(
                    timestamp[0], timestamp[1], timestamp[2],
                    timestamp[3], timestamp[4], timestamp[5]
                )
                log_entry = "{} [{}] {}\n".format(formatted_time, level, message)
                # print(message)
                with open(self.log_file, "a") as f:
                    f.write(log_entry)
                    if isinstance(message, Exception):
                        sys.print_exception(message, f)
                    f.close()
        except Exception as e:
            print(sys.print_exception(e))

logger = Logger(activado=False)
# Example usage
# logger = Logger()

# try:
#     # Some code that might raise an exception
#     result = 1 / 0
# except Exception as e:
#     str(e.with_traceback())
#     logger.error("An error occurred: {}".format(str(e)))
