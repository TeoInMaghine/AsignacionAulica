<#
Este script hace los pasos necesarios para generar el ejecutable.
Si se ejecuta localmente, es recomendable hacerlo en un ambiente virtual.
Se ejecuta en el workflow de github de empaquetado antes de subir el artefacto.
#>

echo "Extract flet version"
$regex_search = Select-String -Path pyproject.toml -Pattern '"flet\s*==\s*(.*)"'
$FLET_VERSION = $regex_search.Matches.Groups[1].Value
echo "FLET_VERSION=$FLET_VERSION"

echo "Install pip packages needed for building"
python -m pip install --upgrade pip
pip install flet-cli==$FLET_VERSION
pip install --requirement src/plantillas_excel/pip-requirements.txt

echo "Export Excel template assets"
python src\plantillas_excel\clases.py src\assets\plantillas_excel\clases.xlsx

echo "Flet Build Windows"
flet build windows --verbose --no-rich-output --cleanup-app --cleanup-packages

