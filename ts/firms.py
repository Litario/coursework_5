import pathlib
from pathlib import Path

# firms_file_name: Path = pathlib.Path(__file__).name

parts: Path = pathlib.Path(__file__).parts
firms_last_dir = fr"{parts[-2]}\{parts[-1]}"

# p = __file__
# print(p.split('\\')[-1])


firms = ['169209',  # ГУД ВУД
         '64174',  # 2ГИС
         '3344',  # ЛСР
         '12550',  # ПИК
         '1102601',  # Самолет
         '2180488',  # ЭТАЛОН
         '68268',  # Пионер
         '1066018',  # Брусника
         '1594501',  # Велеса
         '2302207',  # КРОСТ
         '988387',  # НЛМК
         '6041',  # Северсталь
         '2160557',  # Генпро
         ]
