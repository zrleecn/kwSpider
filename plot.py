from matplotlib import pyplot as plt
from matplotlib import font_manager
import zh2pinyin
import json
import redis


def plot_java_count(cities, job):
    try:
        redis_client = redis.Redis(host='119.29.204.27', port=9502)
    except ConnectionRefusedError:
        print("服务拒绝连接")
        exit(0)
    city_pin = []
    counts = []
    for city in cities:
        city_pin.append(zh2pinyin.main(city))

    print(city_pin)
    for each in city_pin:
        json_text = redis_client.get(each + job)
        if not json_text:  # 没有相关数据 去爬吧
            pass
        jobs = json.loads(json_text)
        counts.append(len(jobs))

    print(counts)

    if len(counts) > 0 and len(counts) == len(cities):
        # 中文乱码处理
        font = font_manager.FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc')
        # 绘图
        plt.bar(range(len(counts)), counts, align='center')

        # 添加标签
        plt.xlabel('城市', fontproperties=font)
        plt.ylabel('需求量', fontproperties=font)
        # 添加刻度
        plt.xticks(range(len(cities)), cities, fontproperties=font)

        plt.title(str(cities) + "城市" + job + "需求量分析", fontproperties=font)

        # 设置y轴的刻度范围
        plt.ylim(0, max(counts) + 100)
        # 每个条形图添加数值标签
        for i in range(len(counts)):
            plt.text(i, counts[i] + 10, str(round(counts[i], 1)), ha='center')
        plt.plot()
        plt.show()
        plt.savefig("./java_city_count.svg")


if __name__ == '__main__':
    cities = ["北京", "上海", "广州", "天津"]  # 已知深圳拼音转换有bug
    plot_java_count(cities, "java")