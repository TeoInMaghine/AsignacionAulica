import sys, logging
from PyQt6.QtCore import qInstallMessageHandler, QtMsgType, QMessageLogContext

root_logger = logging.getLogger('asignacion_aulica')

qt_logger = logging.getLogger('asignacion_aulica.QT')
qt_message_type_to_logging_level = {
    QtMsgType.QtDebugMsg: logging.DEBUG,
    QtMsgType.QtWarningMsg: logging.WARNING,
    QtMsgType.QtCriticalMsg: logging.CRITICAL,
    QtMsgType.QtFatalMsg: logging.FATAL,
    QtMsgType.QtSystemMsg: logging.INFO,
    QtMsgType.QtInfoMsg: logging.INFO
}

def loggear_mensage_de_QT(msg_type: QtMsgType, context: QMessageLogContext, msg: str):
    qt_logger.log(qt_message_type_to_logging_level[msg_type], msg)

qInstallMessageHandler(loggear_mensage_de_QT)

def loggear_a_stdout(loglevel=logging.DEBUG):
    root_logger.setLevel(loglevel)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        fmt='%(asctime)s %(levelname)8s - %(name)-50s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    ))
    root_logger.addHandler(handler)
