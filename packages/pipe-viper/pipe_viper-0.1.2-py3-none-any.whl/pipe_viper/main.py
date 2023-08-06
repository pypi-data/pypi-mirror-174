from subprocess import PIPE, Popen


def run_pwsh(ps1_file_path):
    try:
        sesh = Popen(
            ["powershell.exe", ps1_file_path], universal_newlines=True, stdout=PIPE
        )
    except Exception as error:
        return error
    finally:
        out, err = sesh.communicate()
        return out, err


def run_pwsh_cmd(command):
    try:
        sesh = Popen(
            ["powershell.exe", command],
            universal_newlines=True,
            stdin=PIPE,
            stdout=PIPE,
        )
    except Exception as error:
        return error
    finally:
        out, err = sesh.communicate()
        return out, err


if __name__ == "__main__":
    run_pwsh()
