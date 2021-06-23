#UDP


##client_server.py


Program has possibility to run in server or client mode. The goal of the program is to transfer files from client to the server.
####Libraries used:
1. socket
2. hashlib
3. sys
4. os
5. time
6. glob
7. threading 
8. datetime

####Version:
1. python 3.8 



To run the program you have to put the following command into the command line. 

```python client_server.py mode```

for example 

```python client_server.py -s``` or ```python client_server.py -c``` but before you run the program please red the full description

###As a Server

```python client_server.py -s``` start by default from my own local ip what is 192.168.1.153 and port 5001. You can configure input parameters of server by adding two additional parameters .For example:

```python client_server.py -s server_ip server_port```  

and use case:  ```python client_server.py -s 0.0.0.0 5002``` 

downloaded file will be placed in the **output_files** folder with *output_* prefix in the filename.

Logs should be reported to the **log.txt** file.
If the file is downloaded corectly program should print and log this information including md5 hash check. 

###As a client

Client do not have default configuration. To run the program you have to give him full configuration. File which we want to sent to the server should be placed in **input_files** folder. 

e.g.


```python client_server.py -c server_ip server_port filename```

and use case: ```python client_server.py -c 192.168.1.153 5001 newfile```

##file_generator.py
Program has possibility to genererate file filled with random numeric data but of certain size (more or less).

####Libraries used:
1. sys


####Version:
1. python 3.8 

e.g.
```python file_generator.py file_name size in bytes```

and use case:
```python file_generator.py potato 1024```

Created file should be in **input_files** folder with the given name.

- [x] Przyjmowanie parametrów (proszę zaproponować parametry, które będą konieczne/wygodne)

- [x] Uruchamianie odpowiednio serwera/klienta

- [x] Wygenerowanie pliku o losowej zawartości numerycznej i zadanej wielkości

- [x] Wygenerowanie sumy kontrolnej MD5 pliku

- [x] Dzielenie pliku tak, aby nie przekroczyć MTU

- [x] Wysłanie pliku w kawałkach z użyciem UDP (Części powinny być ponumerowane i następnie ułożone wedle kolejności po stronie klienta)

- [x] Wygenerowanie sumy kontrolnej MD5 odebranego pliku

- [x] Porównanie sum kontrolnych i wyświetlenie wyniku. Pliki nie powinny się różnić. W innym przypadku powinien zostać podniesiony wyjątek.

- [ ] Kod powinien zostać napisany w sposób obiektowy z użyciem dziedziczenia i z zachowaniem zasady SOLID 
 

  *|| Niestety zabrakło mi czasu i program wymagałby jeszcze pracy z mojej strony ponieważ SOLID nie jest dla mnie taki jednoznaczy co w połączeniu z brakiem dużego doświadczenia w tworzenia oprogramowania w sposob obiektowy sprawilo ze to mi sie nie udalo ||*

- [ ] Możliwość uruchomienia programu zadaną ilość razy

- [x] Program powinien zawierać stosowne logi

- [x] Podział na kilka plików - według logiki programu

- [ ] Użycie rekurencji

*|| Probowalem zaimplementowac funkcje do mergowania plikow, ale python ograniczal mi ilosc uzycia rekurencji wiec maksymalny plik jaki moglbyc przesylany to 15Mb w sumie. Do tego tez potrzebowal bym chwili czasu. ||*

- [x] Dodatkowe funkcjonalności niewpływające na bazową funkcjonalność np. pomiar czasu albo logowanie do pliku


#TBD
- GUI
- TESTS
- Recursion
- SOLID - OOP (on higher lever)
- resposne from server to client

*Chętnie nauczye się jak robić takie zadania na wyższym poziomie*



 


