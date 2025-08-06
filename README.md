Anonimizador E-Anônimo: Criptografia de Dados
==============================================

Este projeto é uma aplicação desktop em Python para anonimização e revelação de dados sensíveis em textos, arquivos PDF e Word. Desenvolvido para facilitar a proteção de informações pessoais e sigilosas, especialmente em documentos oficiais.

Funcionalidades
---------------
- **Anonimização de Dados**: Substitui CPFs, CNPJs, nomes, telefones, endereços, apelidos comerciais e outros dados sensíveis por tokens criptografados.
- **Revelação de Dados**: Restaura o texto original a partir do texto anonimizado e do arquivo de mapa JSON gerado.
- **Suporte a múltiplos formatos**: Aceita arquivos .txt, .pdf e .docx.
- **Interface gráfica amigável**: Desenvolvida com Tkinter, com abas para Início, Anonimizar, Revelar e Sobre.
- **Uso de NLP**: Utiliza spaCy (modelo pt_core_news_sm) para identificar entidades nomeadas (pessoas, organizações, locais, etc).

Como Usar
---------
1. **Navegue pelas abas**:
   - **Início**: Tela de boas-vindas.
   - **NotebookLm**: Utilizar para o envio do prompt padrão e apresentar a contextualização para anexar os arquivos já criptografados. 
   - **Anonimizar**: Carregue ou cole o texto, clique em "Anonimizar Texto" e salve o texto anonimizado e o mapa JSON.
   - **Revelar**: Carregue o texto anonimizado e o mapa JSON correspondente para restaurar o texto original.
   - **Sobre**: Manual de uso e informações dos autores.

Exemplo de Uso
--------------
1. Carregue um arquivo ou cole o texto na aba "Anonimizar".
2. Clique em "Anonimizar Texto".
3. Salve o texto anonimizado e o mapa JSON.
4. Para reverter, vá na aba "Revelar", carregue o texto anonimizado e o mapa JSON, e clique em "Revelar Texto Original".

Observações
-----------
- O mapa JSON é indispensável para reverter a anonimização.
- Não utilize para fins ilícitos ou sem autorização.

Desenvolvido por:
-------
- Matheus Brazão (matheus.paixao@antt.gov.br)
- Pedro Cavalcante (pedro.cavalcante@antt.gov.br)

Versão
------
2.1.3 - Ago/2025

Licença
-------
Ferramenta desenvolvida para uso institucional ANTT/GEAUT/COAUT. Consulte os autores para mais informações.
