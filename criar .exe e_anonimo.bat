pyinstaller --onefile --noconsole --icon=e_anonimo.ico --name=E-Anonimo ^
  --add-data "C:\python\Anominizador-de-dados\README.pdf;Anominizador-de-dados" ^
  --add-data "antt_logo.png:." ^
  --collect-all pt_core_news_sm ^
  e_anonimo.py