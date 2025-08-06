import argparse

from lib.pre_release import PreRelease
from lib.release import Release


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--release", action="store_true")
    parser.add_argument("--prerelease", action="store_true")
    args = parser.parse_args()

    if args.release:
        Release().release()
    elif args.prerelease:
        PreRelease().pre_release()


if __name__ == "__main__":
    main()
