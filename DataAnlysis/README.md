# 数据分析

这里主要是做的视频总体数据分析，单个视频的分析代码放到了后端`Backend`文件夹中。总体分析分为视频标题词频分析和视频Tags分析。

## 1 视频标题词频统计

区别于实验2，我们的数据直接从MongoDB数据库中获取并转化为Spark DataFrame，然后再通过select函数取出视频标题数据并转化为Spark RDD，再通过MapReduce整合成为一个字符串并进行数据清洗（去除特殊字符等），然后进行分词并转化为新的RDD对象进行MapReduce从而统计词频，最后将结果转化为Spark Dataframe并存储到MongoDB中。

具体实现在本文件夹的`title_word_count.py`中。

## 2 视频Tag分析

数据收集时tags是以英文逗号分隔的，因此首先进行split得到tag列表。我们对所有视频的tags要进行两项分析：一是统计tag的逐月变化趋势；二是统计tag之间的关联度。前者可以帮助大家了解最近的热点，后者可以有助于我们在分析数据时进行分类和归纳。

（1） tag逐月变化趋势。由于tag数量较少，我们直接进行单机统计。使用二维map进行统计，第一维key代表月份，第二维key代表tag，value代表数量。具体过程如下：

①  对于一个tag列表（包含月份），我们首先用月份做第一层索引。

②  遍历tag作为第二层索引来对该月的tag出现频率进行统计（+1）。

（2）tag间关联度分析。我们同样使用一个二维map来进行统计，第一维和第二维key都是tag，value表示他们一起出现的次数，很容易发现这个map是一个对称矩阵。具体过程如下：

①  对于一个tag列表我们从中取出任意两个tag，记作tag1和tag2。

②  将tag1作为一层索引，tag2作为二层索引，对value+1。

③  将tag2作为一层索引，tag1作为二层索引，对value+1。

④  重复上述过程直到统计完成。

⑤  对于给定的两个tag（u、v），要计算其关联度，我们使用如下公式：

$$
r(u,v)=\frac{2\times\mathrm{count}(u,v)}{\sum_t^{t\in D_u}\mathrm{count}(u,t)+\sum_t^{t\in D_v}\mathrm{count}(t,v)}
$$

其中count函数就对应上述的二维map。这个指标很好地衡量了一个tag在另一个tag中的占比，从而反映了这两个tag之间的关联程度。

可以发现，计算tag间关联度是一个时空复杂度都为$O(n^2)$的算法，而在本项目中tag的数量*n*=495145，这样需要的时间和空间都是很大的。因此，我们并没有采用离线计算并在调用时返回的方式，而是采用用户指定tag，我们在线进行计算的方式。因为这样tag数量是有限的（<20），尽管是$O(n^2)$的算法，在线计算的速度也是很快。

具体实现见`tags_analysis.py`。

## 代码运行

（1）视频词频统计

进入装好`Hadoop(2.10.2)`+`Spark(3.1.3)`的集群环境中，向`Spark`提交`DataAnalysis`中的`title_word_count.py`即可（请保证`Hadoop`和`Spark`集群均打开）。指令如下：

```
/usr/local/spark/bin/spark-submit title_word_count.py
```

环境要求：`python>=3.6`，`jieba>=0.42.1`

（2）Tags分析

直接运行`DataAnlysis`中的`tags_analysis.py`即可。

环境要求：`python>=3.8`，`pymongo>=3.9.0`，`tqdm`

（3）其他

由于后端后续还需要用到各种比率，因此我们需要更新一下数据库，计算出相应的比例。

直接`pythoon process_database.py`即可。
