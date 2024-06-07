import subprocess


def main():
    print("Starting Django server")
    process = subprocess.run(["python", "manage.py", "runserver"])
    if process.returncode == 0:
        print("Server started successfully")
        print(process.stdout)
    else:
        print("Server failed to start")
        print(process.stderr)

if __name__ == "__main__":
    main()  