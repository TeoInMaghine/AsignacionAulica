import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import ModelosAsignaciónÁulica
import QML.ComponentesUI

ListView {
    id: view

    required property int indexCarrera

    spacing: 10
    Layout.preferredWidth: contentItem.childrenRect.width
    Layout.preferredHeight: contentHeight

    model: ListMaterias {
        id: materias
        indexCarrera: view.indexCarrera
    }

    header: Item {
        height: headerMaterias.height + view.spacing
        width: headerMaterias.width

        Label {
            id: headerMaterias
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.bottomMargin: view.spacing
            anchors.leftMargin: 10

            text: view.count === 0 ?
                  "Todavía no hay materias registradas" :
                  "Materias"
            font.pointSize: FontSize.base
        }
    }

    delegate: ColumnLayout {
        id: editorDeMateria

        readonly property alias indentaciónDeAnidado: colapsador.width

        required property var model
        required property var index

        property alias materia : editorDeMateria.model

        RowLayout {
            id: editorSiempreVisibleDeMateria
            spacing: 0

            Colapsador {
                id: colapsador
                Component.onCompleted: {
                    editorDetallesDeMateria.visible = checked
                }
                onClicked: {
                    editorDetallesDeMateria.visible = checked
                }
            }
            TextFieldConEnter {
                text: materia.nombre
                onEditingFinished: {
                    print(editorSiempreVisibleDeMateria.height)
                    print(editorDeMateria.height)
                    materia.nombre = text
                }
            }
            BotónBorrar {
                Layout.leftMargin: 10
                onClicked: {
                    materias.removeRow(index)
                }
            }
        }

        ColumnLayout {
            id: editorDetallesDeMateria
            Layout.leftMargin: indentaciónDeAnidado

            spacing: 10

            RowLayout {
                Label {
                    text: "Año:"
                }
                TextFieldConEnter {
                    Layout.preferredWidth: 50

                    text: materia.año
                    validator: RegularExpressionValidator {
                        // Permitir números positivos o string vacío
                        regularExpression: /^[0-9]*$/
                    }
                    onEditingFinished: {
                        materia.año = text
                    }
                }
            }

            // TODO: Considerar agregar edición de "cuatrimestral o anual"

            Item {
                Layout.alignment: Qt.AlignVCenter | Qt.AlignLeft
                Layout.preferredHeight: editorDeClases.height
                Layout.preferredWidth: editorDeClases.width

                Rectangle {
                    id: fondo
                    anchors.fill: parent

                    color: "#F0F0F0"
                    border.width: 1
                    border.color: "lightgray"
                }
                Clases {
                    id: editorDeClases
                    indexCarrera: view.indexCarrera
                    materia: editorDeMateria.materia
                }
            }

            // Espacio separador (sólo cuando las materias están expandidas)
            Item { height: 10 }
        }

    }

    footer: Item {
        height: footerMaterias.height + footerMaterias.anchors.topMargin
        width: footerMaterias.width

        BotónRedondeadoConTexto {
            id: footerMaterias
            text: "+ Materia"
            anchors.top: parent.top
            anchors.left: parent.left
            // No agregar "spacing" cuando están el header y footer juntos
            anchors.topMargin: view.count === 0 ? 0 : view.spacing
            anchors.leftMargin: 10

            onClicked: {
                materias.insertRow(materias.rowCount())
            }
        }
    }
}
