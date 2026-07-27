from pathlib import Path
import subprocess


class GitService:

    def __init__(self):

        # Repository root (vitesse-control-center/)
        self.repository = Path(__file__).resolve().parents[3]

    def _run(self, *args):

        try:

            result = subprocess.run(
                ["git", *args],
                cwd=self.repository,
                capture_output=True,
                text=True,
                check=True,
            )

            return result.stdout.strip()

        except subprocess.CalledProcessError as exc:

            message = exc.stderr.strip()

            if not message:
                message = exc.stdout.strip()

            raise RuntimeError(message)

    def _run_output(self, *args):

        try:

            result = subprocess.run(
                ["git", *args],
                cwd=self.repository,
                capture_output=True,
                text=True,
                check=True,
            )

            output = result.stdout.strip()
            error = result.stderr.strip()

            return "\n".join(filter(None, [output, error]))

        except subprocess.CalledProcessError as exc:

            message = exc.stderr.strip()

            if not message:
                message = exc.stdout.strip()

            raise RuntimeError(message)

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

        output = self._run("status", "--short")

        if not output:
            return []

        files = []

        for line in output.splitlines():

            status = line[:2].strip()
            path = line[3:].strip()

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