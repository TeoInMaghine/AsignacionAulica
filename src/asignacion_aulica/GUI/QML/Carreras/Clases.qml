import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import ModelosAsignaciónÁulica
import QML.ComponentesUI

ListView {
    id: view

    required property int indexCarrera
    required property var materia
    readonly property int padding: 20

    spacing: headerItem.spacing
    leftMargin: padding
    rightMargin: padding
    topMargin: padding
    bottomMargin: padding

    width: contentItem.childrenRect.width + 2 * padding
    height: contentHeight + 2 * padding

    model: ListClases {
        id: clases
        indexCarrera: view.indexCarrera
        indexMateria: materia.index
    }

    header: Item {
        property alias spacing: headerClases.spacing
        property alias widthDía: headerClases.widthDía
        property alias widthVirtual: headerClases.widthVirtual
        property alias widthCantidadDeAlumnos: headerClases.widthCantidadDeAlumnos
        property alias widthEquipamientoNecesario: headerClases.widthEquipamientoNecesario
        property alias widthAulaAsignada: headerClases.widthAulaAsignada
        height: headerClases.height + view.spacing
        width: headerClases.width

        HeaderClases {
            id: headerClases
            visible: view.count != 0
        }
        Label {
            Layout.margins: 10
            text: "Todavía no hay clases registradas"
            visible: view.count === 0
            font.pointSize: FontSize.medium
        }
    }

    delegate: RowLayout {
        id: editorDeClase
        spacing: headerItem.spacing

        // Referencia: https://doc.qt.io/qt-6/qtquick-modelviewsdata-modelview.html#models

        required property var model
        required property var index

        property alias clase : editorDeClase.model

        SelectorDeDía {
            Layout.preferredWidth: headerItem.widthDía
            currentIndex: clase.día
            onActivated: (index) => {
                clase.día = index
            }
        }

        EditorRangoHorarioClase {
            clase: editorDeClase.clase

            // Usar el ancho que no incluye los side buttons
            Layout.preferredWidth: Constantes.width_editores_horarios
        }

        CheckBox {
            Layout.preferredWidth: headerItem.widthVirtual

            checked: clase.virtual
            onToggled: {
                clase.virtual = checked
            }
        }

        TextFieldConEnter {
            Layout.preferredWidth: headerItem.widthCantidadDeAlumnos

            text: clase.cantidad_de_alumnos
            validator: RegularExpressionValidator {
                // Permitir números positivos o string vacío
                regularExpression: /^[0-9]*$/
            }
            onEditingFinished: {
                clase.cantidad_de_alumnos = text
            }
        }

        SelectorEquipamiento {
            Layout.preferredWidth: headerItem.widthEquipamientoNecesario
            model: ListEquipamientosNecesariosDeClases {
                id: equipamientoNecesario
                indexCarrera: view.indexCarrera
                indexMateria: materia.index
                indexClase: clase.index
            }
        }

        RowLayout {
            Layout.preferredWidth: headerItem.widthAulaAsignada
            spacing: Constantes.spacing_horario

            // TODO: Editar el aula asignada (posiblemente de la misma forma
            // que el edificio preferido de una carrera?)
            Label {
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                // Enfatizar texto cuando se "lockea" la asignación de aula
                font.bold: clase.no_cambiar_asignación
                text: clase.aula_asignada
            }
            Candado {
                Layout.preferredWidth: Constantes.width_horario_sideButtons
                Layout.preferredHeight: Constantes.width_horario_sideButtons

                checked: clase.no_cambiar_asignación
                onClicked: clase.no_cambiar_asignación = checked
            }
        }

        // Item { } // Espacio vacío de 2 * spacing de ancho
        // TODO: Considerar si dejamos ingresar los datos "opcionales"

        BotónBorrar {
            onClicked: {
                clases.removeRow(index)
            }
        }
    }

    footer: Item {
        height: footerClases.height + view.spacing
        width: footerClases.width

        BotónRedondeadoConTexto {
            id: footerClases
            text: "+ Clase"
            anchors.bottom: parent.bottom

            onClicked: {
                clases.insertRow(clases.rowCount())
            }
        }
    }
}
