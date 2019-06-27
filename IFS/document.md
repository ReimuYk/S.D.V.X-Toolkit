# 调用约定

1. 拆解ifs文件，得到tex中的content部分**C**
2. 调用DecompressLSZZ(**C**)得到rawdata **R**
3. 

# 核心函数及其功能逻辑

## DecompressLSZZ

对于上述content **C**的数据分析

1. 前四bytes为固定值

2. 5-8 bytes是后续长度，也就是整个rawdata长度-8

   big-endian保存，宽度为4 bytes

3. 后续为mask和payload交叉排列

   **mask(1 bytes)**，8bits，决定payload的类型，每bit对应一小节payload，顺序为由后往前

   **payload(1 bytes)**，mask为1时的payload，反映为输出结果中的一字节，内容为payload的内容

   **payload(2 bytes)**，mask为0时的payload，前12位表示offset(记为off)，后4位表示length-3(将加三后的值记为len)，复读前述生成的输出结果，offset表示相对输出结尾的偏移，len表示复读长度，若复读长度超过off，则从off偏移开始重新循环直到复读到指定长度，off为0代表payload结束。

解析完rawdata应当得到722\*722\*4长度的输出结果

## DecodeRaw

对于上述输出rawdata **R**的数据分析

R是一个一维数组，里面存的是像素信息（RGBA）

每四 bytes为一个像素，排列为[ B G R A ]

