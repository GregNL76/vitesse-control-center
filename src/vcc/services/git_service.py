import subprocess

from src.vcc.config import PROJECT_ROOT


class GitService:

    def __init__(self):

        # Repository root (vitesse-control-center/)
        self.repository = PROJECT_ROOT

    def _run_command(self, *args):

        try:
            result = subprocess.run(
                ["git", *args],
                cwd=self.repository,
                capture_output=True,
                text=True,
                check=True,
            )

            # Porcelain status records use leading spaces as significant XY
            # status columns. Only remove trailing line endings here.
            stdout = result.stdout.rstrip("\r\n")
            stderr = result.stderr.strip()

            return stdout, stderr

        except subprocess.CalledProcessError as exc:
            message = exc.stderr.strip() or exc.stdout.strip()
            raise RuntimeError(message)

    def _run(self, *args):

        stdout, _ = self._run_command(*args)
        return stdout

    def _run_output(self, *args):

        stdout, stderr = self._run_command(*args)
        return "\n".join(filter(None, [stdout, stderr]))

    def commit_and_push(self, message: str) -> str:

        self._run_output("add", ".")

        if not self._run("status", "--short"):
            return "Nothing to commit.\nWorking tree clean."

        output = []
        output.append(self._run_output("commit", "-m", message))
        output.append(self._run_output("push"))

        return "\n".join([line for line in output if line])

    def branch(self) -> str:

        return self._run("branch", "--show-current")

    def last_commit(self) -> dict:

        output = self._run(
            "log",
            "-1",
            "--pretty=format:%H|%h|%s|%cr",
        )

        full_hash, short_hash, message, relative = output.split("|", 3)

        return {
            "hash": full_hash,
            "short_hash": short_hash,
            "message": message,
            "relative": relative,
        }

    def modified_files(self) -> list:

        output = self._run("status", "--porcelain=v1")

        return self._parse_porcelain(output)

    @staticmethod
    def _parse_porcelain(output: str) -> list:

        if not output:
            return []

        files = []

        for line in output.splitlines():

            if len(line) < 4 or line[2] != " ":
                raise RuntimeError(f"Unexpected git status --porcelain=v1 output: {line!r}")

            status = line[:2].strip()
            path = line[3:]

            files.append(
                {
                    "status": status,
                    "path": path,
                }
            )

        return files

    def status(self) -> dict:

        files = self.modified_files()

        return {
            "repository": self.repository.name,
            "branch": self.branch(),
            "clean": len(files) == 0,
            "modified_count": len(files),
            "last_commit": self.last_commit(),
            "files": files,
        }