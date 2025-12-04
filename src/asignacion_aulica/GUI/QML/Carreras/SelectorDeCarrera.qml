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

    property int índiceDeLaCarreraActual: comboBox.currentIndex

    property bool estamosEditandoElNombre: false
    
    ListCarreras { id: modelo_de_carreras }

    Label{
        text: "Carrera: "
        font.pointSize: FontSize.big
    }

    ComboBoxCarrera{
        id: comboBox
        modelo_de_carreras: modelo_de_carreras
        visible: !estamosEditandoElNombre
    }

    TextField {
        id: inputEditarNombre
        visible: estamosEditandoElNombre
        Layout.preferredHeight: comboBox.height
        Layout.preferredWidth: comboBox.Layout.preferredWidth

        onAccepted: {
            var nuevoÍndice = modelo_de_carreras.cambiarNombre(comboBox.currentIndex, inputEditarNombre.text)
            comboBox.currentIndex = nuevoÍndice
            estamosEditandoElNombre = false
        }

        Keys.onEscapePressed: {
            estamosEditandoElNombre = false
        }
    }

    BotónRedondeadoConTexto {
        text: "Editar Nombre"
        enabled: comboBox.hayCarreraSeleccionada
        icon.source: assets_path + "/iconos/editar.png"
        onClicked: {
            inputEditarNombre.text = comboBox.currentText
            inputEditarNombre.focus = true
            estamosEditandoElNombre=true
        }
    }

    BotónRedondeadoConTexto {
        text: "Borrar Carrera"
        enabled: comboBox.hayCarreraSeleccionada
        icon.source: assets_path + "/iconos/Borrar.svg"
        onClicked: confirmaciónBorrar.open()
    }

    // Solamente visible al clickear el botón de borrar:
    Dialog {
        id: confirmaciónBorrar
        title: "¿Borrar la carrera?"
        standardButtons: Dialog.Ok | Dialog.Cancel

        onAccepted: {
            var nuevoÍndice = modelo_de_carreras.borrarCarrera(comboBox.currentIndex)
            comboBox.currentIndex = nuevoÍndice
        }

        width: 450 // Si no se define un esto, da error: QML Dialog: Binding loop detected for property "implicitWidth"

        Text {
            text: "Se perderá toda la información de la carrera " + comboBox.currentText + "."
            wrapMode: Text.Wrap
            width: parent.width
        }
    }
}
