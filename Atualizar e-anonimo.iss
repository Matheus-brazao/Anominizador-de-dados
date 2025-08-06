[Setup]
AppName= E-Anônimo
AppVersion=2.1.4
DefaultDirName={localappdata}\E-Anônimo
DefaultGroupName=E-Anônimo
OutputBaseFilename=E-Anônimo
// NÃO MEXA NESSAS OPÇÕES //////////////////
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest
/////////////////////////////////////////////
[Files]
Source: "C:\python\Anominizador-de-dados\dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs
Source: "C:\python\Anominizador-de-dados\dist\README.pdf"; DestDir: "{app}\Anominizador-de-dados"; Flags: ignoreversion
// MANTENHA O PADRÃO "\*" NO FINAL DO CAMINHO 
// PARA INDICAR QUE VAI SER UTILIZADO OS ARQUIVOS 
// DAQUELA PASTA EM ESPECIFICO
/////////////////////////////////////////////

// IDIOMA DO INSTALADOR, PADRÃO PORTUGUES ///
[Languages]
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"
/////////////////////////////////////////////
// DECLARAR ATALHOS DO PROGRAMA ((PADRÃO))
[Icons]
Name: "{userdesktop}\E-Anônimo"; Filename: "{app}\E-Anonimo.exe"  
Name: "{userdesktop}\Desinstalar E-Anônimo"; Filename: "{uninstallexe}"

// ATALHOS OPCIONAIS DEPENDENDO DO PROGRAMA, COMO PASTA DE DOWNLOAD OU PLANILHAS EXCEL


/////////////////////////////////////////////
// CODIGO PADRÃO APENAS MUDE A FUNÇÃO DO PROGRAMA
[Code]
var
  CustomPage: TWizardPage;
  TermsPage: TInputOptionWizardPage;
  MemoText: TMemo; // Declara a variável MemoText

procedure InitializeWizard;
begin
  // Cria uma página personalizada
  CustomPage := CreateCustomPage(wpWelcome, 'Informações Importantes', 'Leia as informações abaixo antes de continuar.');

  // Adiciona um memo na página de informações
  MemoText := TMemo.Create(CustomPage);
  MemoText.Parent := CustomPage.Surface;
  MemoText.ScrollBars := ssVertical; // Adiciona uma barra de rolagem vertical
  MemoText.ReadOnly := True; // Torna o texto somente leitura
  MemoText.WordWrap := True; // Habilita quebra de linha automática
  MemoText.TabStop := False; // Impede que o controle receba foco ao pressionar Tab
  MemoText.Text := 'Este programa não armazena nenhuma informação como Login, Senha ou dados sensíveis respeitando a LGPD' +
    ' e foi desenvolvido para automatizar tarefas para fins de criptografia, ' +
    'permitindo verificar o envio de Editais e gerar relatório no formato de Log. Ao utilizar este software, você concorda com os seguintes termos:' + #13#10#13#10 +
    '1. Uso Responsável: O programa deve ser utilizado apenas para fins legais e autorizados. O usuário é responsável por garantir que possui permissão no E-Anônimo.' + #13#10#13#10 +
    '2. Limitação de Responsabilidade: O desenvolvedor não se responsabiliza por quaisquer danos, perdas ou consequências decorrentes do uso do programa, incluindo erros no sistema que resultam falhas na automação.' + #13#10#13#10 +
    '3. Privacidade e Segurança: O usuário é responsável por proteger suas credenciais e garantir que elas não sejam compartilhadas ou utilizadas de forma inadequada.';
    
  MemoText.Top := 10;
  MemoText.Left := 10;
  MemoText.Width := CustomPage.SurfaceWidth - 20;
  MemoText.Height := CustomPage.SurfaceHeight - 20;

  // Cria uma nova página para os Termos de Uso
  TermsPage := CreateInputOptionPage(CustomPage.ID,
    'Termos de Uso',
    'Leia e aceite os Termos de Uso para continuar',
    'Você deve aceitar os Termos de Uso para instalar o programa.',
    True, False);

  // Adiciona a caixa de seleção para aceitar os Termos de Uso
  TermsPage.Add('Eu li e aceito os Termos de Uso.');

  // Define a caixa de seleção como desmarcada por padrão
  TermsPage.Values[0] := False;
end;

function NextButtonClick(CurPageID: Integer): Boolean;
begin
  // Verifica se o usuário está na página de Termos de Uso
  if CurPageID = TermsPage.ID then
  begin
    // Se a caixa de seleção não estiver marcada, exibe uma mensagem de erro
    if not TermsPage.Values[0] then
    begin
      MsgBox('Para instalar esse programa, é necessário aceitar os Termos de Uso.', mbError, MB_OK);
      Result := False; // Impede que o usuário avance
      Exit;
    end;
  end;

  Result := True; // Permite que o usuário avance
end;

// O READEME.pdf DEVE SER ESPECIFICAMENTE DO PROGRAMA NO FORMATO PDF
[Run]
Filename: "{app}\Anominizador-de-dados\README.pdf"; Description: "Abrir instruções do programa"; Flags: postinstall shellexec skipifsilent