import argparse

from .password import PasswordGenerator as Pg
from .exception import ZenpassException

__prog__ = 'zenpass'
__version__ = '1.0.2'


def get_argument():
    parser = argparse.ArgumentParser(prog=__prog__, usage="zenpass [options]")
    parser.add_argument('-v', '--version', action='version', help='show version number and exit.', version=__version__)
    group = parser.add_argument_group("to customize Password")
    group.add_argument("-l", "--length", dest="length", type=int, metavar='', help="to set length to the password")
    group.add_argument("-n", "--ignore", dest="ignore", metavar='',
                       help="to ignore unwanted characters to the password")
    group.add_argument("-i", "--include", dest="include", metavar='', help="to include characters to the password")
    group.add_argument("-o", "--only", dest="only", metavar='', help="to create password only using wanted characters")
    group.add_argument("-s", "--separator", dest="separator", metavar='', help="the separator character")
    group.add_argument("-c", "--seplen", dest="separatorlength", type=int, metavar='',
                       help="the length of characters between separator")
    group.add_argument("--repeat", dest="repeat", action='store_true', default=False,
                       help="to repeat the characters in the password (default : %(default)s)")
    group.add_argument("--separation", dest="separation", default=False, action="store_true",
                       help="to separate password characters using separator (default : %(default)s)")
    group.add_argument("--show", dest="show", default=False, action="store_true",
                       help="to show password (default : %(default)s)")
    parser.add_argument_group(group)
    options = parser.parse_args()
    return options


def generate_password(rep: bool, separation: bool, pass_len=None, wanted=None, ign=None, inc=None, sep=None,
                      sep_len=None, show: bool = False):
    Pg(length=pass_len, only=wanted, ignore=ign, include=inc, repeat=rep, separator=sep,
       separator_length=sep_len, separation=separation).generate(show)


def main():
    try:
        options = get_argument()
        generate_password(options.repeat, options.separation, options.length, options.only, options.ignore,
                          options.include, options.separator, options.separatorlength, options.show)
    except ZenpassException as e:
        print(e.__str__())


if __name__ == "__main__":
    main()
