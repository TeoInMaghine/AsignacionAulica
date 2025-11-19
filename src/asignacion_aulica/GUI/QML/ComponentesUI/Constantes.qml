import QtQuick

pragma Singleton

QtObject {
    readonly property color rojo_unrn: "#EB1C38"
    readonly property color rojo_unrn_oscuro: "#B70C0C"
    readonly property color rojo_unrn_oscurísimo: "#730202"

    readonly property int width_columna_horario: 100
    readonly property string ícono_colapsador_path:
        assets_path + "/iconos/Colapsador.svg"
    readonly property string ícono_candado_cerrado_path:
        assets_path + "/iconos/CandadoCerrado.svg"
    readonly property string ícono_candado_abierto_path:
        assets_path + "/iconos/CandadoAbierto.svg"
}
