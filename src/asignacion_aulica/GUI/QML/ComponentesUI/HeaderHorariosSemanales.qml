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
    /* El texto con el nombre de la semana tiene que estar alineado con
     * los editores de horarios, no con los "side buttons".
     * Por eso metemos el Label adentro del RowLayout, le ponemos ancho igual a
     * los editores de horarios y alineamos hacia la izquierda.
     */
    RowLayout {
        required property string modelData

        Layout.preferredWidth: Constantes.width_columna_horario

        Label {
            Layout.preferredWidth: Constantes.width_editores_horarios
            Layout.alignment: Qt.AlignVCenter | Qt.AlignLeft

            horizontalAlignment: Text.AlignHCenter
            text: modelData
        }
    }
}
