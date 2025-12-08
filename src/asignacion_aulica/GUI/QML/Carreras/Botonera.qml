import QtQuick.Controls
import QtQuick.Layouts
import QML.ComponentesUI
import ModelosAsignaciónÁulica

/** Los botones de arriba de la pestaña de materias. */
RowLayout {
    spacing: 15

    property var gestor: ProxyGestorDeDatos{}

    // Por ahora no hacen nada
    BotónRedondeadoConTextoColorUNRN {
        text: "Asignar Aulas"
        onClicked: gestor.asignarAulas()
    }
    BotónRedondeadoConTextoColorUNRN {text: "Exportar Excel"}
    BotónRedondeadoConTextoColorUNRN {text: "Importar Excel"}
}
