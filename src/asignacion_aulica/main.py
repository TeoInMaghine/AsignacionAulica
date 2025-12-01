import sys
import logging
from asignacion_aulica.GUI.main import main as gui_main
from asignacion_aulica import logging_config

logger = logging.getLogger('asignacion_aulica.main')

def main():
    logging_config.loggear_a_stdout()

    logger.info('---------- Iniciando el programa ----------')
    exit_code = gui_main()
    logger.info('---------- El programa terminó con código %s ----------', exit_code)
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
