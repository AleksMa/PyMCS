# Поиск максимального общего подграфа

В общем случае принимаем файлы, содержащие несколько графов.  
Происходит полный перебор возможных пар, удовлетворяющих статистической гипотезе,
с проверкой алгоритмом VF2 подграфов меньшего графа на subgraph-изоморфность большему графу алгоритмом VF2.

Результат работы - мера схожести для наиболее близких пар.

## Использование

```bash
python3 run.py /data/graph.txt /data/pattern.txt 0.8 60 0.99
```