import QtQuick

pragma Singleton

QtObject {
    readonly property color rojo_unrn: "#EB1C38"
    readonly property color rojo_unrn_oscuro: "#B70C0C"
    readonly property color rojo_unrn_oscurísimo: "#730202"

    readonly property int fontsize_pts_base: 12 // También definido en main.py
    readonly property int fontsize_pts_medium: 15
    readonly property int fontsize_pts_big: 17
    readonly property int fontsize_pts_bigger: 20
    readonly property int fontsize_pts_huge: 28

    readonly property int width_columna_horario: 100
    readonly property string ícono_colapsador_path:
        assets_path + "/iconos/Colapsador.svg"
}
