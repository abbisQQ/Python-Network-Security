# HTTP file interceptor. 
When the victim tries to download any .exe files we capture the packet and redirect the request to wherever we like.
This only works for http!

As we can see from the image below the victim clicks to download a win-zip21.exe file and instead it gets a wrar file.
Notice that you must be the man in the middle in order to perform this on other computers in your network.

![Screenshot from 2019-04-21 11-31-03](https://user-images.githubusercontent.com/21143253/56472546-dae11200-642d-11e9-8dab-bc69b6ae99ef.png)
