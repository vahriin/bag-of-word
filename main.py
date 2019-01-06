import math
from preparing import load, count_words_by_tags, to_file


def bag_of_words(counters):
    bag = {}
    order_of_add = {}
    for order, (tag, counter) in enumerate(counters.items()):
        order_of_add[order] = tag
        for word, freq in counter.items():
            tf = freq / len(counter)
            idf = math.log(len(counters) / how_many(word, counters))
            if word in bag.keys():
                f_list = make_list(len(counters.keys()), order, tf * idf)
                bag[word] = add_lists(bag[word], f_list)
            else:
                bag[word] = make_list(len(counters.keys()), order, tf * idf)
    return bag, order_of_add


def guess_tag(news_list, bag, order):
    tags = []
    for news in news_list:
        result_vec = [0 for _ in order.keys()]
        for word in news.body:
            if word in bag.keys():
                result_vec = add_lists(result_vec, bag[word])
        index = result_vec.index(max(result_vec))
        tags.append(order[index])
    return tags


def how_many(word, counters):
    res = 0
    for counter in counters.values():
        if word in counter:
            res += 1
    return res


def make_list(len_, order, value):
    assert order < len_
    result = [-value for x in range(len_)]
    result[order] *= -1
    return result


def add_lists(list1, list2):
    assert len(list1) == len(list2)
    result = [0 for _ in range(len(list1))]
    for i in range(len(list1)):
        result[i] = list1[i] + list2[i]
    return result


def main():
    news = load("news_train.txt")
    counters = count_words_by_tags(news)
    bag, order = bag_of_words(counters)
    test = load("news_test.txt")
    tags = guess_tag(test, bag, order)
    to_file("result.txt", tags)


if __name__ == "__main__":
    main()
