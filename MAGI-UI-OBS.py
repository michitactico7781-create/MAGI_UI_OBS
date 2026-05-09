import sys

def check_package(package_name, import_name=None):
    if import_name is None:
        import_name = package_name
    try:
        __import__(import_name)
        print(f"✅ {package_name} - OK")
        return True
    except ImportError:
        print(f"❌ {package_name} - FALTA INSTALAR")
        return False

print("=== VERIFICANDO DEPENDENCIAS DE MAGI v4.0 ===\n")

packages = [
    ("streamlit", "streamlit"),
    ("groq", "groq"),
    ("fpdf", "fpdf"),
    ("edge-tts", "edge_tts"),
    ("pygame", "pygame"),
    ("requests", "requests"),
    ("beautifulsoup4", "bs4"),
]

all_ok = True
for pkg, imp in packages:
    if not check_package(pkg, imp):
        all_ok = False

print("\n" + "="*40)
if all_ok:
    print("🎉 TODAS LAS DEPENDENCIAS ESTÁN INSTALADAS CORRECTAMENTE")
    print("\nPara ejecutar MAGI:")
    print("streamlit run magi_v4.py")
else:
    print("⚠️ FALTAN DEPENDENCIAS. Ejecuta:")
    print("pip install streamlit groq fpdf edge-tts pygame requests beautifulsoup4")
