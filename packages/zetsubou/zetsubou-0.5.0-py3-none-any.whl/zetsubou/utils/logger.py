import sys
import traceback
from enum import Enum
from colorama import Fore, Style, Back
from colorama import init as colorama_init
from zetsubou.utils.error_codes import EErrorCode


class ELogLevel(Enum):
    Verbose = 0
    Info = 1
    Warning = 2
    Error = 3
    Critical = 4
    Silent = 5


class scope_level:
    level: ELogLevel
    prev: ELogLevel

    def __init__(self, level: ELogLevel):
        self.level = level

    def __enter__(self):
        self.prev = LoggerStorage.log_level
        SetLogLevel(self.level)

    def __exit__(self, exc_type, exc_val, exc_tb):
        SetLogLevel(self.prev)


class LoggerStorage:
    log_level : ELogLevel = ELogLevel.Info


def Initialize():
    colorama_init()


def SetLogLevel(log_level : ELogLevel):
    LoggerStorage.log_level = log_level


def IsVisible(level : ELogLevel):
    if level.value < LoggerStorage.log_level.value:
        return False
    return True


def ReturnCode(code: EErrorCode):
    if code == 0x0:
        Success('Returned code 0')
    elif IsVisible(ELogLevel.Critical):
        print(f'{Fore.RED}{Back.WHITE} Returned error code {code.value} - {code.name} {Style.RESET_ALL}')


def CriticalError(err):
    if IsVisible(ELogLevel.Critical):
        print('')
        print(f'{Fore.WHITE}{Back.RED} {err} {Style.RESET_ALL}')


def Exception(ex):
    if IsVisible(ELogLevel.Error):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        msg = 'Exception occured, '.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        Error(msg)


def Error(err):
    if IsVisible(ELogLevel.Error):
        print('')
        print(f'{Fore.RED}{err}{Style.RESET_ALL}')


def Warning(warn):
    if IsVisible(ELogLevel.Warning):
        print(f' - {Fore.YELLOW}{warn}{Style.RESET_ALL}')


def Info(inf):
    if IsVisible(ELogLevel.Info):
        print(f' - {inf}')


def Success(suc):
    if IsVisible(ELogLevel.Info):
        print(f' - [{Fore.GREEN}ok{Style.RESET_ALL}] {suc}')


def Loading(type: str, name: str):
    if IsVisible(ELogLevel.Info):
        print(f' - Loading [{Fore.LIGHTBLUE_EX}{type}{Style.RESET_ALL}] \'{name}\'')


def Command(name: str):
    if IsVisible(ELogLevel.Info):
        print(f'\n - Command [{Fore.CYAN}{name}{Style.RESET_ALL}]')


def Verbose(verb):
    if IsVisible(ELogLevel.Verbose):
        print(f' - {verb}')
