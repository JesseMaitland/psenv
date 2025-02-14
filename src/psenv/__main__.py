from psenv.cli import parse_psenv_args


def main() -> int:
    cliargs = parse_psenv_args()
    return cliargs.command(cliargs=cliargs)()


if __name__ == "__main__":
    exit(main())
