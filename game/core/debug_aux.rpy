
init -1 python:
    DebugLog.base_path=config.basedir
    DEBUG=DebugLog()
    DEBUG.reset()
    DEBUG.print("Debug log file\n"+
    "To use,add \"DEBUG.print(<stuff>)\" to your code\n"+
    "To reset, add \"DEBUG.reset()\"")