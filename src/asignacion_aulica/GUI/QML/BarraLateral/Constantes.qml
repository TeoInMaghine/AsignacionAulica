import QtQuick

pragma Singleton

QtObject {
    readonly property color rojo_unrn: "#EB1C38"
    readonly property color rojo_unrn_oscuro: "#B70C0C"
    readonly property color rojo_unrn_oscurísimo: "#730202"
    
    readonly property int ancho_de_la_barra: 230

    readonly property string título_texto: "Asignación Áulica"
    readonly property int título_tamaño: 28

    readonly property string logo_unrn_path: assets_path + "/logo_unrn_blanco.svg"
    readonly property int logo_unrn_margen: 15

    readonly property int pestaña_altura: 55
    readonly property int pestaña_texto_altura: 20
}
