import pyautogui

x, y = pyautogui.position()
print ("Posicao atual do mouse:")
print ("pyautogui.click("+str(x)+","+str(y)+")")

#retorna True se x & y estiverem dentro da tela
print ("\nEsta dentro da tela?")
resp = pyautogui.onScreen(x, y)
print (resp)
input()