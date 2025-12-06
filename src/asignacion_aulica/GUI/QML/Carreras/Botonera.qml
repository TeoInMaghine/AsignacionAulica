import QtQuick.Controls
import QtQuick.Layouts
import QML.ComponentesUI

/** Los botones de arriba de la pestaña de materias. */
RowLayout {
    spacing: 15

    // Por ahora no hacen nada
    BotónRedondeadoConTextoColorUNRN {text: "Asignar Aulas"}
    BotónRedondeadoConTextoColorUNRN {text: "Exportar Excel"}
    BotónRedondeadoConTextoColorUNRN {text: "Importar Excel"}
}
