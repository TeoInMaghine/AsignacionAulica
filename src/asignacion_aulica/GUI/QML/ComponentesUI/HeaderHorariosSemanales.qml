import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Repeater {
    model: [
        "Lunes",
        "Martes",
        "Miércoles",
        "Jueves",
        "Viernes",
        "Sábado",
        "Domingo"
    ]
    Label {
        Layout.preferredWidth: Constantes.width_columna_horario
        horizontalAlignment: Text.AlignHCenter

        required property string modelData
        text: modelData
    }
}
