1. Cнос старой версии PyTorch без CUDA и установка версии с CUDA
>```shell
> pip uninstall torch
>```
>```shell
>pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117
>```
2. Установка [CUDA](https://developer.nvidia.com/cuda-downloads) с офицального сайта и обновление драйверов видеокарты

3. Проверка CUDA 
>```shell
>python3 cuda.py
>```
> Проверка ручками
>```py
>import torch
>x = torch.rand(5, 3)
>y = torch.cuda.is_available()
>print(x)
>print(y)
>```
> Output similar to:
>```py
>tensor([[0.3380, 0.3845, 0.3217],
>        [0.8337, 0.9050, 0.2650],
>        [0.2979, 0.7141, 0.9069],
>        [0.1449, 0.1132, 0.1375],
>        [0.4675, 0.3947, 0.1426]])
>True
>```
Нормализация собранных статей
>```shell
>python3 normalization.py
>```
Обучние модели
>```shell
> singleLabel.ipynb
>```
Проверка модели
>```shell
> result.ipynb
>```
