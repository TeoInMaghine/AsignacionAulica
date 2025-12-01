import QtQuick
import QML.ComponentesUI

pragma Singleton

QtObject {    
    readonly property int ancho_de_la_barra: 230

    readonly property string título_texto: "Asignación Áulica"

    readonly property string logo_unrn_path: assets_path + "/logo_unrn_blanco.svg"
    readonly property int logo_unrn_margen: 15

    readonly property int pestaña_altura: 55
}
