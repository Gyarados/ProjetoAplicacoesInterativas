import pyautogui
import speech_recognition as sr
import pyaudio

pyautogui.FAILSAFE = False

running = False

# for i in range(pyaudio.PyAudio().get_device_count()):
#     print(pyaudio.PyAudio().get_device_info_by_index(i))

click_1_commands = ["clica", "clique", "click", 'esquerdo']
click_2_commands = ["clica direito", "clique direito", "click direito", 'direito']
scroll_commands = ['scroll', 'rodinha', 'rola', 'roda', 'rolamento']
double_click_commands = ['entrar', 'duplo', 'double', 'dois']

#Função para ouvir e reconhecer a fala
def ouvir_microfone(root=None):
    #Habilita o microfone do usuário
    recognizer = sr.Recognizer()
    
    #usando o microfone
    with sr.Microphone() as source:
        
        #Chama um algoritmo de reducao de ruidos no som
        recognizer.adjust_for_ambient_noise(source)
        
        #Frase para o usuario dizer algo
        print("Diga alguma coisa: ")
    
        try:
            #Armazena o que foi dito numa variavel
            audio = recognizer.listen(source, phrase_time_limit=3)
            print("Processando...")
        except sr.WaitTimeoutError:
            print("Não escutei")
            return

    try:
        
        #Passa a variável para o algoritmo reconhecedor de padroes
        frase: str = recognizer.recognize_google(audio,language='pt-BR')

        frase_lower = frase.lower()
        if frase_lower in click_1_commands:
            pyautogui.click()  
        if frase_lower in click_2_commands:
            pyautogui.rightClick()  
        if frase_lower in scroll_commands:
            pyautogui.middleClick()   
        if frase_lower in double_click_commands:
            pyautogui.doubleClick()
        # if "clica" in frase.lower() or "clique" in frase.lower() or "click" in frase.lower():
        #     pyautogui.click()  
        #Retorna a frase pronunciada
        print("Você disse: " + frase)
        
    #Se nao reconheceu o padrao de fala, exibe a mensagem
    except sr.UnknownValueError:
        print("Não entendi")
    
    if root:
        root.update()
        root.after(0, ouvir_microfone(root))


def activate():
    global running
    while running:
        ouvir_microfone()
    
if __name__ == "__main__":
    try:
        running = True
        activate()
    except Exception as e:
        print(e)
