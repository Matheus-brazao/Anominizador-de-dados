[Setup]
AppName= E-An�nimo
AppVersion=2.1.4
DefaultDirName={localappdata}\E-An�nimo
DefaultGroupName=E-An�nimo
OutputBaseFilename=E-An�nimo
// N�O MEXA NESSAS OP��ES //////////////////
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest
/////////////////////////////////////////////
[Files]
Source: "C:\python\Anominizador-de-dados\dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs
Source: "C:\python\Anominizador-de-dados\dist\README.pdf"; DestDir: "{app}\Anominizador-de-dados"; Flags: ignoreversion
// MANTENHA O PADR�O "\*" NO FINAL DO CAMINHO 
// PARA INDICAR QUE VAI SER UTILIZADO OS ARQUIVOS 
// DAQUELA PASTA EM ESPECIFICO
/////////////////////////////////////////////

// IDIOMA DO INSTALADOR, PADR�O PORTUGUES ///
[Languages]
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"
/////////////////////////////////////////////
// DECLARAR ATALHOS DO PROGRAMA ((PADR�O))
[Icons]
Name: "{userdesktop}\E-An�nimo"; Filename: "{app}\E-Anonimo.exe"  
Name: "{userdesktop}\Desinstalar E-An�nimo"; Filename: "{uninstallexe}"

// ATALHOS OPCIONAIS DEPENDENDO DO PROGRAMA, COMO PASTA DE DOWNLOAD OU PLANILHAS EXCEL


/////////////////////////////////////////////
// CODIGO PADR�O APENAS MUDE A FUN��O DO PROGRAMA
[Code]
var
  CustomPage: TWizardPage;
  TermsPage: TInputOptionWizardPage;
  MemoText: TMemo; // Declara a vari�vel MemoText

procedure InitializeWizard;
begin
  // Cria uma p�gina personalizada
  CustomPage := CreateCustomPage(wpWelcome, 'Informa��es Importantes', 'Leia as informa��es abaixo antes de continuar.');

  // Adiciona um memo na p�gina de informa��es
  MemoText := TMemo.Create(CustomPage);
  MemoText.Parent := CustomPage.Surface;
  MemoText.ScrollBars := ssVertical; // Adiciona uma barra de rolagem vertical
  MemoText.ReadOnly := True; // Torna o texto somente leitura
  MemoText.WordWrap := True; // Habilita quebra de linha autom�tica
  MemoText.TabStop := False; // Impede que o controle receba foco ao pressionar Tab
  MemoText.Text := 'Este programa n�o armazena nenhuma informa��o como Login, Senha ou dados sens�veis respeitando a LGPD' +
    ' e foi desenvolvido para automatizar tarefas para fins de criptografia, ' +
    'permitindo verificar o envio de Editais e gerar relat�rio no formato de Log. Ao utilizar este software, voc� concorda com os seguintes termos:' + #13#10#13#10 +
    '1. Uso Respons�vel: O programa deve ser utilizado apenas para fins legais e autorizados. O usu�rio � respons�vel por garantir que possui permiss�o no E-An�nimo.' + #13#10#13#10 +
    '2. Limita��o de Responsabilidade: O desenvolvedor n�o se responsabiliza por quaisquer danos, perdas ou consequ�ncias decorrentes do uso do programa, incluindo erros no sistema que resultam falhas na automa��o.' + #13#10#13#10 +
    '3. Privacidade e Seguran�a: O usu�rio � respons�vel por proteger suas credenciais e garantir que elas n�o sejam compartilhadas ou utilizadas de forma inadequada.';
    
  MemoText.Top := 10;
  MemoText.Left := 10;
  MemoText.Width := CustomPage.SurfaceWidth - 20;
  MemoText.Height := CustomPage.SurfaceHeight - 20;

  // Cria uma nova p�gina para os Termos de Uso
  TermsPage := CreateInputOptionPage(CustomPage.ID,
    'Termos de Uso',
    'Leia e aceite os Termos de Uso para continuar',
    'Voc� deve aceitar os Termos de Uso para instalar o programa.',
    True, False);

  // Adiciona a caixa de sele��o para aceitar os Termos de Uso
  TermsPage.Add('Eu li e aceito os Termos de Uso.');

  // Define a caixa de sele��o como desmarcada por padr�o
  TermsPage.Values[0] := False;
end;

function NextButtonClick(CurPageID: Integer): Boolean;
begin
  // Verifica se o usu�rio est� na p�gina de Termos de Uso
  if CurPageID = TermsPage.ID then
  begin
    // Se a caixa de sele��o n�o estiver marcada, exibe uma mensagem de erro
    if not TermsPage.Values[0] then
    begin
      MsgBox('Para instalar esse programa, � necess�rio aceitar os Termos de Uso.', mbError, MB_OK);
      Result := False; // Impede que o usu�rio avance
      Exit;
    end;
  end;

  Result := True; // Permite que o usu�rio avance
end;

// O READEME.pdf DEVE SER ESPECIFICAMENTE DO PROGRAMA NO FORMATO PDF
[Run]
Filename: "{app}\Anominizador-de-dados\README.pdf"; Description: "Abrir instru��es do programa"; Flags: postinstall shellexec skipifsilent