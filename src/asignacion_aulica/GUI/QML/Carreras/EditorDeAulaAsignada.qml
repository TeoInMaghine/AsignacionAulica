import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QML.ComponentesUI
import ModelosAsignaciónÁulica

RowLayout {
    required property int indexCarrera
    required property int indexMateria
    required property int indexClase
    
    SelectorDeEdificioConAulas{
        id: selectorEdificio
        Layout.preferredWidth: Constantes.width_editor_edificio
    }

    SelectorDeAula{
        indexEdificio: selectorEdificio.indexEdificioSeleccionado
        Layout.preferredWidth: Constantes.width_editor_aula
    }
}
