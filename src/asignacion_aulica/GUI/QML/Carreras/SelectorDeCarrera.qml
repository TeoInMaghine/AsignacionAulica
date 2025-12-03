import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QML.ComponentesUI
import ModelosAsignaciónÁulica

/** Dropdown para seleccionar carrera.
 *  También permite agregar, borrar, y cambiar nombre.
 */
RowLayout {
    spacing: 10

    Label{
        text: "Carrera: "
        font.pointSize: FontSize.big
    }

    ComboBoxCarrera{ id: comboBox }

    BotónRedondeadoConTexto {
        text: "Cambiar Nombre"
        enabled: comboBox.hayCarreraSeleccionada
    }

    BotónRedondeadoConTexto {
        text: "Borrar Carrera"
        enabled: comboBox.hayCarreraSeleccionada
        onClicked: confirmaciónBorrar.open()
    }

    // Diálogo solamente visible al clickear el botón de borrar:
    Dialog {
        id: confirmaciónBorrar
        title: "¿Borrar la carrera?"
        standardButtons: Dialog.Ok | Dialog.Cancel

        onAccepted: {
            console.log("Ok clicked")
            comboBox.borrar()
        }
        onRejected: console.log("Cancel clicked")

        width: 450 // Si no se define un esto, da error: QML Dialog: Binding loop detected for property "implicitWidth"

        Text {
            text: "Se perderá toda la información de la carrera " + comboBox.currentText + "."
            wrapMode: Text.Wrap
            width: parent.width
        }
    }
}
