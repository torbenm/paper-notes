import sys

logger_prefix = ""


def set_prefix(prefix):
    global logger_prefix
    logger_prefix = prefix


def progress(step, total):
    global logger_prefix
    epsilon = 0.00001
    percent = (float(step) / (total+epsilon)) * 100
    out = '{0} [ {2:100} ] {1:07.4f}% '.format(
        logger_prefix, percent, "|" * int(percent))
    sys.stdout.write("\r" + out)
    sys.stdout.flush()
