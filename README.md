Detector de Movimento com OpenCV 🕵️‍♂️⚡

Resumo rápido: este script em Python usa OpenCV para detectar movimento a partir da webcam, aguarda um curto período para “estabilizar” o movimento e então salva um frame em JPG (apenas um por evento de movimento). Ideal como base para vigilância leve, captura de evidências ou gatilho para envio a uma API.

✨ Recursos principais

Detecção baseada em background subtraction (MOG2).

Filtragem morfológica para reduzir ruído.

Lógica simples de estado (in_motion) para não disparar várias capturas durante o mesmo evento.

Delay configurável antes de enviar/salvar o frame (evita frames de transição).

Timeout configurável para resetar o estado quando o movimento para.

🚀 Uso rápido

Pressione q para sair da aplicação.

🔧 Parâmetros importantes (e o que significam)

Dentro do código:

fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=True)

motion_timeout = 3      # segundos sem movimento para resetar in_motion
delay_capture = 2       # espera (segundos) desde o início do movimento até salvar o frame


Outros parâmetros operacionais:

history (MOG2): quantos frames o modelo usa para estimar o background.

varThreshold (MOG2): sensibilidade ao movimento (menor -> mais sensível).

contourArea > 5000: área mínima do contorno para considerar movimento (aumente/diminua conforme câmera/ambiente).

kernel = (5,5) na morfologia: afeta remoção de ruído (maior kernel = mais suavização).

🧠 Como funciona (passo a passo)

Captura frame da webcam.

Aplica o BackgroundSubtractorMOG2 para obter máscara (foreground).

Executa morphologyEx (OPEN) para remover ruído.

Detecta contornos na máscara e verifica se algum tem área > 5000.

Se movimento detectado:

Se é o primeiro frame do evento, marca last_motion_time e define in_motion = True.

Se já está em movimento e passou delay_capture, salva o frame (cv2.imwrite(...)) e atualiza last_motion_time para evitar envio repetido.

Se não há movimento e já estava em movimento, aguarda motion_timeout para resetar in_motion = False e permitir a próxima detecção.

Mostra o frame em janela (cv2.imshow). Fecha ao pressionar q.

✅ Exemplo de saída (prints exibidos)
Movimento estabilizado! Enviando frame...
Movimento encerrado. Pronto para próxima detecção.


Os arquivos JPG gerados terão nome baseado no timestamp: 169XXXXX...jpg.
