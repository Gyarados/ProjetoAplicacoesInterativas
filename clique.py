import pyautogui
import speech_recognition as sr
import asyncio
import pyaudio

for i in range(pyaudio.PyAudio().get_device_count()):
    print(pyaudio.PyAudio().get_device_info_by_index(i))


#Função para ouvir e reconhecer a fala
def ouvir_microfone():
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
            print(audio)
            print("Processando...")
        except sr.WaitTimeoutError:
            print("Não escutei")
            return

    try:
        
        #Passa a variável para o algoritmo reconhecedor de padroes
        frase: str = recognizer.recognize_google(audio,language='pt-BR')
        if "clica" in frase.lower() or "clique" in frase.lower() or "click" in frase.lower():
            pyautogui.click()  
        #Retorna a frase pronunciada
        print("Você disse: " + frase)
        
    #Se nao reconheceu o padrao de fala, exibe a mensagem
    except sr.UnknownValueError:
        print("Não entendi")


def main():
    while True:
        ouvir_microfone()
    
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
