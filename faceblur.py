import sys
import cv2
import imutils

# Menu de ajuda
def printHelp():
    helpString = '=== Faceblur ===\n' \
    'Detecção e anonimização de faces em imagens e vídeos.\n\n' \
    'Como usar: faceblur <caminho_do_arquivo>\n\n' \
    'Formatos permitidos: PNG, JPG e MP4\n' \
    'Exemplo: faceblur /home/user/imagens/foto.jpg\n\n' \
    'Para utilizar a câmera, use o id do dispositivo como caminho do arquivo.\n' \
    'Exemplo: faceblur 0'
    print(helpString)
    sys.exit(1)

# Printa mensagem de erro
def printError(error):
    print('Erro: ' + error)
    printHelp()

# Verifica se a quantidade de argumentos é válida ou se o argumento é -h ou --help
if (len(sys.argv) < 2 or len(sys.argv) > 2 or sys.argv[1] == '-h' or sys.argv[1] == '--help'):
    printHelp()

# Verifica se é câmera ou se o arquivo existe
def checkFilePath(filePath):
    if (filePath.isnumeric()):
        return "camera"
    else:
        try:
            open(filePath)
        except IOError:
            printError('Arquivo não encontrado')

        # Verifica se o arquivo é uma imagem ou um vídeo
        if (filePath.endswith('.png') or filePath.endswith('.jpg') or filePath.endswith('.jpeg')):
            return "imagem"
        elif (filePath.endswith('.mp4')):
            return "video"
        else:
            printError('Formato de arquivo inválido')

def blurFaces(filePath, fileType):
    print('Pressione "q" para sair...')
    classificador = cv2.CascadeClassifier('cascades/haarcascade_frontalface_alt.xml')

    if (fileType == "imagem"):
        imagem = cv2.imread(filePath)
        imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

        facesDetectadas = classificador.detectMultiScale(imagemCinza)

        for (x, y, largura, altura) in facesDetectadas:
            blur = imagem[y:y+altura, x:x+largura]
            blur = cv2.GaussianBlur(blur, (23,23), 30)
            imagem[y:y+blur.shape[0], x:x+blur.shape[1]] = blur

        while (cv2.waitKey(1) != ord('q')):
            cv2.imshow("Faceblur - " + filePath, imagem)
    elif (fileType == "video" or fileType == "camera"):
        if (fileType == "camera"):
            filePath = int(filePath)

        video = cv2.VideoCapture(filePath)

        while True:
            conectado, frame = video.read()

            frame = imutils.resize(frame, width=720)

            frameCinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            facesDetectadas = classificador.detectMultiScale(frameCinza)
            
            for (x, y, largura, altura) in facesDetectadas:
                blur = frame[y:y + altura, x:x + largura]
                blur = cv2.GaussianBlur(blur, (27, 27), 30)
                frame[y:y + blur.shape[0], x:x + blur.shape[1]] = blur
            cv2.imshow("Faceblur - " + str(filePath), frame)
            if(cv2.waitKey(1) == ord('q')):
                break
        video.release()
        cv2.destroyAllWindows()
    else:
        printError('Erro desconhecido')

# Caminho do arquivo
filePath = sys.argv[1]

# Tipo de arquivo
fileType = checkFilePath(filePath)

# Executa o programa
blurFaces(filePath, fileType)
