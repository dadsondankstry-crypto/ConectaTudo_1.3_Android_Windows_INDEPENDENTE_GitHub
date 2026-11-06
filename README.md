# ConectaTudo 1.3 — Android + Windows (instalação paralela)

Projeto completo para **Gerenciador GitHub → GitHub Actions → APK + EXE**, com ambos workflows na raiz. O Android 1.3 usa o **`applicationId br.app.conectatudo.v13`** e instala ao lado das versões antigas. O executável e o instalador Windows são identificados como **1.3**, com AppId de Inno Setup distinto.

## Novidades da 1.3

1. **Controle remoto temporário do Windows** a partir do navegador Android: cliques na tela, clique direito e duplo, rolagem, teclas de navegação e digitação de texto. O programa Windows deve estar com **Compartilhar tela** ativo e o dono deve apertar **Permitir controle (15 min)**. Isso gera um **código extra de 12 números**; é necessário informar tanto esse código quanto o PIN de rede. É possível bloquear imediatamente; após 15 minutos o código expira. Controle remoto de Android **não está implementado**.
2. **Compartilhamento da tela por MJPEG** na interface web, reduzindo a sobrecarga de uma requisição por imagem. Ainda é uma série de JPEGs, não transmissão H.264 em 30/60 fps; atrasos podem ocorrer. O Windows permite selecionar Econômico, Equilibrado ou Nítido.
3. **Transferência em blocos** pelo **painel web** (`/`): pausar, continuar, cancelar e retomar o mesmo arquivo após uma falha, *enquanto o servidor receptor estiver ativo*. Reabra o mesmo painel e selecione novamente o mesmo arquivo (mesmo nome e tamanho). O protocolo original `/api/send` continua disponível para envio nativo nos aplicativos Android/Windows. **Pausa/retomada ainda não funciona nos botões nativos** do APK/EXE.
4. **Conexão online por VPN privada já configurada**: conecte o POCO e o Legion Go (ou tablet) à mesma rede privada do Tailscale ou equivalente e informe **IP da VPN + PIN**. Nesse caso, podem estar em Wi-Fis diferentes e usar internet. A criptografia do trajeto é fornecida pela VPN, não pelo HTTP do app.
5. Mantidos QR no Android, IP+PIN sem câmera no Windows, descoberta em LAN, envio de arquivos e pastas ZIP do Windows, mensagens automáticas, status e progresso.

## IMPORTANTE: o que NÃO está implementado

- **Não há servidor de intermediação público, sinalização automática P2P, NAT traversal ou retransmissão TURN.** A VPN privada é uma solução externa que exige instalação/autenticação e conexão nos dois aparelhos. O ConectaTudo **não instala nem cria essa VPN sozinho**. A descoberta por broadcast só funciona dentro da LAN, não automaticamente por VPN.
- O protocolo do ConectaTudo ainda usa **HTTP sem TLS próprio** e PIN de seis dígitos. Para redes distantes, use VPN privada que cifre o tráfego entre os dois dispositivos. **Nunca abra/encaminhe a porta TCP 8765 à internet pública**. Não use Wi-Fi público desprotegido.
- O controle do Windows ainda não permite arrastar/soltar, transferir áudio, controlar UAC ou a tela bloqueada. Algumas teclas e programas elevados não aceitarão comandos.
- **Não há transferência criptografada ponta a ponta pelo próprio app, checksum SHA-256 por arquivo, nem retomada de envio nativo do APK/EXE**. Ainda faltam testes de desempenho e segurança em aparelhos reais.

## Como usar offline na mesma rede

1. Conecte os aparelhos ao mesmo Wi-Fi ou hotspot e abra apenas **uma versão do ConectaTudo por vez** em cada dispositivo (porta TCP **8765**, descoberta UDP **39402**).
2. No Windows, dê acesso de firewall **somente em rede privada** se solicitado; copie o IP e o PIN. No Android, informe os dados ou toque em Procurar dispositivos / Ler QR.
3. Para compartilhar a tela, autorize no emissor. No Windows marque *Compartilhar tela*. Para controlar Windows: clique *Permitir controle (15 min)*, no celular toque *Controlar Legion Go*, informe o **código extra** e interaja com a imagem.
4. Para arquivos com pausa/retomada, no aparelho que está enviando abra o **painel do destino** no navegador, selecione o arquivo e use Pausar / Continuar. Para retomar após falha, selecione novamente o mesmo arquivo **antes de fechar o servidor de destino**.

## Como usar pela internet com VPN privada

1. Instale **Tailscale** (ou solução equivalente) no Windows e no Android, seguindo o serviço escolhido. Faça login e confirme que ambos aparecem na mesma rede privada.
2. Abra o ConectaTudo 1.3 nos dois dispositivos, preferencialmente usando redes confiáveis. No Legion Go, identifique o IP da VPN (geralmente começa com `100.`). No Android, digite esse IP e o PIN exibido no Windows. Se necessário, permita o ConectaTudo no firewall Windows **apenas para o perfil privado/VPN**.
3. Teste **Conectar**. Não espere que **Procurar aparelhos** descubra automaticamente um IP remoto pela VPN.
4. Se quiser controlar o Windows, ele precisa estar com compartilhamento de tela e autorização temporária ativos. Você controla e pode interromper a qualquer momento no Windows.

## Gerar APK e EXE pelo GitHub Actions

Envie o ZIP completo para a **raiz de um repositório novo** pelo Gerenciador GitHub. Mantenha `.github/workflows/android.yml`, `.github/workflows/windows.yml`, `android/`, `windows/`, `tests/` e este README na raiz (não coloque pasta adicional).

- **`ConectaTudo-Android-1.3-INDEPENDENTE-APK`** → `app-debug.apk`, Android 8+ (target SDK 35).
- **`ConectaTudo-Windows-1.3-EXE`** → `ConectaTudo-Windows-1.3.exe` portátil, não precisa Python instalado.
- **`ConectaTudo-Windows-1.3-INSTALADOR`** → opcional, `ConectaTudo-Setup-1.3.exe` (só quando Inno Setup estiver disponível no GitHub Actions).

Windows: Python 3.12 + PyInstaller, pacote `Pillow` para compartilhar tela. Android: Gradle 8.9, AGP 8.7.3, Java 17, Android SDK 35. Os APKs/EXEs podem ser criados no GitHub sem instaladores locais.

## Testes que foram feitos e limitações

- Testes locais em Python (`python -m unittest discover -s tests -v`) passaram para: mensagens, recusa de controle não autorizado e envio de arquivo em partes com retomada e comparação byte a byte do arquivo recebido. O workflow Windows também executa esses testes.
- Sintaxe Python compilada localmente e JavaScript do painel validado com `node --check`; ZIP validado ao final.
- **Não foi feita compilação local do APK Android nem do EXE Windows**, nem teste de controle remoto real, nem ensaio em redes diferentes por VPN. O funcionamento nesses ambientes precisa ser verificado com os APK/EXE gerados pelo GitHub e os dispositivos reais.

**Dados anteriores:** instalar versões em paralelo não migra dados automaticamente. Feche versões antigas antes de iniciar o servidor 1.3 na mesma máquina.
