import cv2
import time


cap = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=True)

in_motion = False
last_motion_time = 0
motion_timeout = 3      # tempo sem movimento para resetar
delay_capture = 2       # segundos para esperar antes de enviar

while True:
    ret, frame = cap.read()
    if not ret:
        break

    fgmask = fgbg.apply(frame)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    movement_detected = any(cv2.contourArea(c) > 5000 for c in contours)

    if movement_detected:
        if not in_motion:
            # Primeiro frame do movimento → só marca tempo
            last_motion_time = time.time()
            in_motion = True

        # Se já passou o delay_capture, envia o frame
        elif time.time() - last_motion_time >= delay_capture:
            print("Movimento estabilizado! Enviando frame...")
            # Salva o frame em jpg na pasta do arquivo do código
            cv2.imwrite(str(time.time()).replace(".","")+".jpg", frame)
            # evita enviar de novo até o movimento encerrar
            last_motion_time = time.time()  

    else:
        # Se não tem movimento por motion_timeout, libera próximo ciclo
        if in_motion and (time.time() - last_motion_time > motion_timeout):
            print("Movimento encerrado. Pronto para próxima detecção.")
            in_motion = False

    cv2.imshow("Deteccao de Movimento", frame)

    if cv2.waitKey(30) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
