# Captura de Mídia Baseada em Navegador com Flask e OpenCV 📸

Este projeto é uma aplicação web desenvolvida em Python e JavaScript que demonstra a integração entre o backend de um servidor e as APIs de hardware nativas do navegador. O script simula uma interface de "Confirmação de Acesso" que solicita permissão de câmera para registrar uma presença de forma automatizada.

O projeto possui caráter estritamente **educacional e de auditoria**, servindo para demonstrar os mecanismos de permissão e transferência de dados binários via requisições HTTP.

---

## ⚠️ AVISO LEGAL (Disclaimer)

Este repositório foi criado exclusivamente para fins didáticos, laboratoriais e de conscientização sobre segurança da informação. O uso deste código para coletar imagens ou dados de indivíduos sem o consentimento explícito, informado e legal dos mesmos é de total responsabilidade do usuário. O desenvolvedor não apoia e não se responsabiliza por quaisquer atividades maliciosas ou violações de privacidade realizadas com este software.

---

## ⚙️ Mecanismo de Funcionamento

1. **Servidor Backend:** O micro-framework `Flask` inicializa um servidor local que escuta na porta `5000`.
2. **Requisição de Mídia:** Ao acessar a rota principal, o navegador renderiza uma interface e utiliza a API `navigator.mediaDevices.getUserMedia` para solicitar acesso ao dispositivo de vídeo padrão (`facingMode: "user"`).
3. **Renderização Oculta:** O elemento `<video>` e o `<canvas>` são mantidos com a propriedade CSS `style="display:none;"` para fins de simulação de processos em segundo plano.
4. **Captura e Conversão:** Ao clicar no botão de confirmação, o JavaScript desenha o frame atual da câmera no elemento canvas e extrai a string em formato **Base64** (`data:image/jpeg;base64,...`).
5. **Processamento de Imagem:** O servidor Python recebe a string Base64, decodifica os dados binários e utiliza a biblioteca `OpenCV (cv2)` para reconstruir a matriz de imagem (`imdecode`) e salvá-la localmente com uma estampa de tempo (*timestamp*).

---

## 🛠️ Tecnologias e Bibliotecas Utilizadas

*   **Linguagem Principal:** Python 3.x
*   **Web Framework:** [Flask](https://palletsprojects.com) (Rotas e renderização de string de template)
*   **Processamento Digital de Imagens:** [OpenCV (opencv-python)](https://opencv.org) (Manipulação de arrays binários e salvamento de arquivos)
*   **Manipulação de Matrizes:** [NumPy](https://numpy.org) (Conversão de buffer de bytes para array de dados)
*   **Interface:** HTML5 / JavaScript (MediaDevices API & Fetch API)

---

## 📦 Estrutura de Diretórios Gerada

Após a execução bem-sucedida e a primeira captura, a aplicação cria automaticamente a pasta para armazenamento:

```text
├── app.py                # Código principal do servidor Flask
├── fotos/                # Diretório criado automaticamente pelo script
│   └── foto_AAAAMMDD_HHMMSS.jpg  # Registro salvo com data e hora
└── requirements.txt      # Dependências do projeto
```

---

## 🚀 Como Executar o Projeto

### 1. Clonar o Repositório
```bash
git clone https://github.com
cd seu-repositorio
```

### 2. Instalar as Dependências
Crie um arquivo chamado `requirements.txt` e adicione as bibliotecas utilizadas pelo script:
```text
Flask
opencv-python
numpy
```
Em seguida, instale-as executando:
```bash
pip install -r requirements.txt
```

### 3. Iniciar o Servidor
Execute o arquivo principal do script:
```bash
python app.py
```
O servidor estará ativo em `http://localhost:5000` ou no IP da sua rede local `http://0.0.0`.

---

## 🔒 Restrições Importantes de Segurança (HTTPS)

Os navegadores modernos implementam políticas rígidas baseadas no conceito de **Contextos Seguros**:
*   A API `getUserMedia` só funcionará se o site for servido através de uma conexão **HTTPS** criptografada.
*   A única exceção a essa regra é o endereço `localhost` ou `127.0.0.1`, permitindo que este script seja testado e validado em ambiente de desenvolvimento local sem certificados SSL adicionais.
