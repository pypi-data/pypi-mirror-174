from zetsubou.utils.subprocess import call_process
import zetsubou.utils.logger as logger
from typing import List


def check_conan_present():
    out, err = call_process(['conan', '--version'], capture=True, realtime=False)
    if err is not None:
        logger.CriticalError('Conan is missing, unable to proceed')
        return False

    logger.Success("Conan present")
    logger.Verbose(out)
    return True


def call_conan(args : List[str], cwd : str):
    verbose = logger.IsVisible(logger.ELogLevel.Verbose)
    out, err = call_process(['conan'] + args, capture = not verbose, realtime = verbose, cwd = cwd)
    if err is not None:
        if not verbose:
            logger.CriticalError(f'Conan command failed: {" ".join(args)}')
            logger.Error(out)

        logger.CriticalError(f"Conan returned error '{err}'")
        return False
    return True
