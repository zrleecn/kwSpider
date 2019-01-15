import json
import redis


def get_date_by_key(key):
    redis_client = redis.Redis(host='119.29.204.27', port=9502)
    if redis_client.exists(key):
        return redis_client.get(key)
    return None


def store_csv(key):
    """保存到csv中"""

    data_str = get_date_by_key("php")
    if data_str:
        items = json.loads(data_str)
    csv = open(key + ".csv", "w+")
    if items:
        for item in items:
            # print(item)
            csv.write(item['job_name'] + "," + item['company'] + "," +
                      item['salary'][0] + "," + item['education'] + "," + str(item['job_wel']) + "\r\n")

    csv.close()


if __name__ == '__main__':

    store_csv("php")





