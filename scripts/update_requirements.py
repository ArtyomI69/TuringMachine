import subprocess

if __name__ == '__main__':
    # Run the command and capture the stdout
    process = subprocess.Popen(["pip","freeze"], stdout=subprocess.PIPE)
    stdout_bytes = process.communicate()[0]

    # Convert bytes to string
    stdout_str = stdout_bytes.decode('utf-8')
    stdout_str = stdout_str.replace("==", ">=")
    open("../requirements.txt", "w").write(stdout_str)