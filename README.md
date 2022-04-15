# CSVDriveAPIUploader

Script criado para realizar o download de infinitos CSV's da plataforma Google Docs e realizar o upload deles em uma pasta no Google Drive de forma automática.

Como utilizar:

Abra no Google Spreadsheets os documentos que deseja usar no script.
Clique em Arquivo -> Compartilhar -> Publicar na Web
Selecione a página que deseja exportar e selecione o formato CSV.
Em caso de múltiplas páginas, exporte uma a uma.
Copie o link fornecido.

Com os links coletados, acesse o arquivo appConfig.py e insira os links na Array "URL's", um link por índice da Array.
Em "destinyFolderID", insira o ID da pasta que receberá os arquivos no Google Drive.
O ID da pasta destino pode ser coletado ao acessar a pasta do Google Drive no navegador, sendo encontrado no URL.

PONTOS DE ATENÇÃO:
* Um arquivo chamado de "credentials.json" deve existir na pasta raiz do projeto, junto aos arquivos app.py e appConfig.py contendo as credenciais do Google Cloud API.
* O projeto no Google Drive API deve conter o Drive API instalado.
* Na primeira vez que o script for ser rodado, é necessário uma máquina com suporte a interface gráfica e navegador web para realizar o login no Google, gerando o arquivo token.json.

