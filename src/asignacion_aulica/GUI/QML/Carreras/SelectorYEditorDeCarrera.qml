import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QML.ComponentesUI
import ModelosAsignaciónÁulica

/** 
 * Se encarga de:
 * - Seleccionar la carrera que se está editando actualmente
 * - Agregar y borrar carreras
 * - Editar el nombre de la carrera seleccionada
 * - Editar propiedades de la carrera seleccionada
 *   (actualmente la única propiedad es el edificio preferido)
 * 
 * No se encargar de editar las materias y clases de la carrera.
 */
ColumnLayout{
    spacing: 10

    ListCarreras { id: listCarreras }

    RowLayout {
        spacing: 10

        Label{
            text: "Carrera: "
            font.pointSize: FontSize.big
        }

        ComboBoxCarrera{
            id: comboBox
            listCarreras: listCarreras
            visible: !inputEditarNombre.focus
        }

        TextField {
            id: inputEditarNombre
            visible: inputEditarNombre.focus
            Layout.preferredHeight: comboBox.height
            Layout.preferredWidth: comboBox.Layout.preferredWidth

            text: comboBox.currentText
            onAccepted: {
                var nuevoÍndice = listCarreras.cambiarNombre(comboBox.currentIndex, inputEditarNombre.text)
                comboBox.currentIndex = nuevoÍndice
                inputEditarNombre.focus = false
            }

            Keys.onEscapePressed: {
                inputEditarNombre.focus = false
            }
        }

        BotónRedondeadoConTexto {
            text: "Editar Nombre"
            enabled: comboBox.hayCarreraSeleccionada
            icon.source: assets_path + "/iconos/editar.png"
            onClicked: {
                inputEditarNombre.focus = true
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
                var nuevoÍndice = listCarreras.borrarCarrera(comboBox.currentIndex)
                comboBox.currentIndex = nuevoÍndice
            }

            width: 450 // Si no se define esto, da error: QML Dialog: Binding loop detected for property "implicitWidth"

            Text {
                text: "Se perderá toda la información de la carrera " + comboBox.currentText + "."
                wrapMode: Text.Wrap
                width: parent.width
            }
        }
    }

    RowLayout {
        spacing: 10

        Label{
            text: "Edificio preferido: "
            font.pointSize: FontSize.base
        }

        SelectorEdificio{
            enabled: comboBox.hayCarreraSeleccionada
            Layout.preferredWidth: 270

            onActivated: indexEdificio => {
                console.log(indexEdificio)
                listCarreras.setEdificioPreferido(comboBox.currentIndex, indexEdificio-1)
            }
        }
    }
}
