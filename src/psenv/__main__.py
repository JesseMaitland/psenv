from dotenv import load_dotenv

from psenv.cli import parse_psenv_args


def main() -> int:
    load_dotenv()
    cliargs = parse_psenv_args()
    return cliargs.command(cliargs=cliargs)()


if __name__ == "__main__":
    exit(main())
