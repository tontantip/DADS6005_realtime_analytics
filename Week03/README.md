# Lab

## 1. Basic setup (My first topic)
```
1.1 Start a kafka cluster --> Double click "1_1_start_cluster.bat"

1.2 Create a topic --> Double click "1_2_create_my_first_topic.bat"

1.3 Start a consumer --> Double click "1_3_run_consumer_my_first_topic.bat"

1.4 Start a producer --> Double click "1_4_run_producer_my_first_topic.bat"

1.5 After finish testing, close all windows.
```

## 2. Word count
```
2.1 Start a kafka cluster --> Double click "2_0_start_cluster.bat"

2.2 Create a topic --> Double click "2_1_create_streams_plaintext_input.bat"

2.3 Start a producer --> Double click "2_2_run_producer_wordcount.bat"

2.4 Start a wordcount program --> Double click "2_3_compile_word_count.bat"
- when success built, click to continue.

2.5 Start a consumer --> Double click "2_4_run_consumer_wordcount.bat"

2.6 Test it. You can type
"a a a" --> then press enter
"a a b" --> then press enter
in the producer window, and you will get 
a 5
b 1 
in the consumer window

2.7 After finish testing, close all windows.

```

## 3. Adding a filter function to word count (Allow only the value which is higher than 10)
```
3.1 Start a kafka cluster --> Double click "3_1_start_cluster.bat".

3.2 Create a topic --> Double click "3_2_create_streams_plaintext_input.bat"

3.3 Start a producer --> Double click "3_3_run_producer_wordcount.bat"

3.4 Modify code and then --> Double click "3_4_compile_word_count.bat" --> If built success, Click to continue.

3.5 Start a new consumer by using python --> Run "python consumer-local-plotgraph.py" for graph-mode version

3.6 Check your result
```

Solution of 3.
``` Java
 final KTable<String, Long> counts = source
            .flatMapValues(value -> Arrays.asList(value.toLowerCase(Locale.getDefault()).split(" ")))
            .groupBy((key, value) -> value)
            .count()
            .filter((key, value) -> value > 10);
```

## Homework1: หาคำที่มีนัยสำคัญ (ไม่ใช่ article a, an ,the, ...) ในนิยาย Harry potter
