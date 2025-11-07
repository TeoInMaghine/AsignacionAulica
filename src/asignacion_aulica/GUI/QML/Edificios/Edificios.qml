import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
// import ModelosAsignaciónÁulica
import QML.ComponentesUI

ListView {
    id: view

    readonly property int indentaciónDeAnidado: 20

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

        required property var model
        required property var index

        property alias edificio : editorDeEdificio.model

        RowLayout {
            id: editorSiempreVisibleDeEdificio

            Colapsador {
                Component.onCompleted: {
                    // Descomentar para facilitar debugging:
                    // checked = true
                    editorDetallesDeEdificio.visible = checked
                    fondoYEditorDeAulas.visible = checked
                }
                onClicked: {
                    editorDetallesDeEdificio.visible = checked
                    fondoYEditorDeAulas.visible = checked
                }
            }
            TextField {
                text: edificio.nombre
                onEditingFinished: {
                    edificio.nombre = text
                }
            }
        }

        RowLayout {
            id: editorDetallesDeEdificio
            Layout.leftMargin: indentaciónDeAnidado

            // Espacio sutil que evita fealdad difícil de explicar entre
            // horarios y checkbox de "Evitar"
            spacing: 10

            ColumnLayout {
                RowLayout { HeaderHorariosSemanales { } }
                RowLayout { EditorHorariosSemanales { } }
            }

            ColumnLayout {
                Label {
                    Layout.alignment: Qt.AlignCenter
                    horizontalAlignment: Text.AlignHCenter
                    text: "Preferir no usar"
                }
                CheckDelegate {
                    // display: CheckDelegate.IconOnly no funciona, idk why
                    Layout.preferredWidth: 52
                    Layout.preferredHeight: 40

                    highlighted: hovered

                    checked: edificio.preferir_no_usar
                    onToggled: {
                        edificio.preferir_no_usar = checked
                    }
                }
            }
        }

        Item {
            id: fondoYEditorDeAulas
            Layout.leftMargin: indentaciónDeAnidado

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
    }

    footer: Item {
        height: footerEdificios.height + view.spacing
        width: footerEdificios.width

        Button {
            id: footerEdificios
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            anchors.leftMargin: 10
            width: 200

            text: "añadir"
            highlighted: hovered
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
