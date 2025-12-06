import QtQuick

pragma Singleton

QtObject {
    readonly property color rojo_unrn: "#EB1C38"
    readonly property color rojo_unrn_oscuro: "#B70C0C"
    readonly property color rojo_unrn_oscurísimo: "#730202"

    readonly property int width_editor_horario: 45
    readonly property int width_horario_sideButtons: 24
    readonly property int spacing_horario: 2
    readonly property int width_editores_horarios:
        2*width_editor_horario + spacing_horario
    readonly property int width_columna_horario:
        width_editores_horarios + spacing_horario + width_horario_sideButtons
    readonly property string ícono_colapsador_path:
        assets_path + "/iconos/Colapsador.svg"
    readonly property string ícono_candado_cerrado_path:
        assets_path + "/iconos/CandadoCerrado.svg"
    readonly property string ícono_candado_abierto_path:
        assets_path + "/iconos/CandadoAbierto.svg"
    readonly property string ícono_reestablecer_path:
        assets_path + "/iconos/Reestablecer.svg"
}
