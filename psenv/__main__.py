from ramjam.utils import parse_args
from psenv import cli


def main() -> int:
    cli_args = parse_args(cli, ignore=["basepsenvcommand"])
    command = cli_args.command(cli_args=cli_args)
    return command()


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
