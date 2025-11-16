import sys
import logging
from asignacion_aulica.GUI.main import main
from asignacion_aulica import logging_config

logger = logging.getLogger('asignacion_aulica.main')

if __name__ == '__main__':
    logging_config.loggear_a_stdout()

    logger.info('---------- Iniciando el programa! ----------')
    exit_code = main()
    logger.info('---------- El programa terminó con código %s ----------', exit_code)
    sys.exit(exit_code)
