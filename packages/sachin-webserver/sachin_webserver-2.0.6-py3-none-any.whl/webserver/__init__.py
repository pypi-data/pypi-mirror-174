def server():
    import os
    print("Please use command-line options")
    try:
        os.system("server --help")
    except:
        print("Perhaps you haven't installed cli-webserver")