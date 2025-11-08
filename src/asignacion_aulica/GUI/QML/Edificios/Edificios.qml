import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
// import ModelosAsignaciónÁulica
import QML.ComponentesUI

ListView {
    id: view

    anchors.fill: parent
    spacing: 10

    width: parent.width
    contentWidth: contentItem.childrenRect.width + 2 * anchors.margins
    // TODO: esto no funciona completamente al achicar la ventana
    ScrollBar.horizontal: ScrollBar { id: hbar; active: vbar.active }
    ScrollBar.vertical: ScrollBar { id: vbar; active: hbar.active }
    flickableDirection: Flickable.HorizontalAndVerticalFlick

    clip: true

    // TODO: reemplazar por modelo
    // model: ListEdificios { id: edificios }
    model: ListModel {
        id: edificios
        ListElement {
            nombre: "Anasagasti I"
            preferir_no_usar: false
        }
        ListElement {
            nombre: "Anasagasti II"
            preferir_no_usar: false
        }
        ListElement {
            nombre: "Tacuarí"
            preferir_no_usar: true
        }
    }

    delegate: ColumnLayout {
        id: editorDeEdificio

        width: view.width

        readonly property alias indentaciónDeAnidado: colapsador.width

        required property var model
        required property var index

        property alias edificio : editorDeEdificio.model

        RowLayout {
            id: editorSiempreVisibleDeEdificio
            spacing: 0

            Colapsador {
                id: colapsador
                Component.onCompleted: {
                    // Descomentar para facilitar debugging:
                    checked = true
                    editorDetallesDeEdificio.visible = checked
                }
                onClicked: {
                    editorDetallesDeEdificio.visible = checked
                }
            }
            TextField {
                text: edificio.nombre
                onEditingFinished: {
                    edificio.nombre = text
                }
            }
        }

        ColumnLayout {
            id: editorDetallesDeEdificio
            Layout.leftMargin: indentaciónDeAnidado

            spacing: 10

            CheckDelegate {
                text: "Preferir no usar"

                highlighted: hovered

                checked: edificio.preferir_no_usar
                onToggled: {
                    edificio.preferir_no_usar = checked
                }
            }
            ColumnLayout {
                RowLayout { HeaderHorariosSemanales { } }
                RowLayout { EditorHorariosSemanales { } }
            }

            Item {
                Layout.alignment: Qt.AlignVCenter | Qt.AlignLeft
                Layout.preferredHeight: editorDeAulas.height
                Layout.preferredWidth: editorDeAulas.width

                Rectangle {
                    id: fondo
                    anchors.fill: parent

                    color: "#F0F0F0"
                    border.width: 1
                    border.color: "lightgray"
                }
                Aulas {
                    id: editorDeAulas
                    edificio: editorDeEdificio.edificio
                }
            }

            // Espacio separador (sólo cuando los edificios están expandidos)
            Item { height: 50 }
        }

    }

    footer: Item {
        height: footerEdificios.height + view.spacing
        width: footerEdificios.width

        BotónAñadir {
            id: footerEdificios
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            anchors.leftMargin: 10
            width: 200

            text: "+"
            onClicked: {
                edificios.append({
                    nombre: "",
                    preferir_no_usar: false
                })
                // edificios.insertRow(edificios.rowCount())
            }
        }
    }
}
