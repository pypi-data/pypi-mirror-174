def desc(data, save=False, number=20, df=None):
    """
    注：通过输入数据应用本方法可以将数据质量直观、全面的展示。
    :param data: 数据的数据
    :param save: 是否需要保存文件到本地
    :param number: 维度字段的维度上限
    :param df: 选择输出的表
                df = 1 输出空值概述
                df = 2 输出维度字段概述
                df = 2 输出度量字段概述
    :return: df
    """
    import pandas as pd
    # 第一
    all_data = []
    for i in range(1, data.shape[1] + 1):
        all_data.append(len(data))

    null_n = list(data.isnull().sum())

    null_b = []
    for i in null_n:
        if i == 0:
            null_b.append('0%')
        else:
            n_b = i / len(data) * 100
            n_b = '%.2f' % n_b
            null_b.append(str(n_b) + '%')

    dfr = []
    for i in list(data):
        dfr.append(len(data[i].unique()))

    lists = [
        all_data,
        null_n,
        null_b,
        dfr,
    ]

    df1 = pd.DataFrame(data=lists, index=['数据总数', '空值个数', '空值比例', '不同值个数'],
                       columns=[list(data)])

    # 第二
    listss = list(data.describe())
    listssa = []
    for i in listss:
        mean = data[i].describe()[1]
        std = data[i].describe()[2]
        min_ = data[i].describe()[3]
        max_ = data[i].describe()[-1]
        M_3 = data[i].describe()[1] - 3 * std
        M3 = data[i].describe()[1] + 3 * std

        j = [min_, max_, mean, std, M_3, M3]
        listssa.append(j)
    df3 = pd.DataFrame(data=listssa, index=listss, columns=['MIN', 'MAX', 'Mean', 'Std', 'M-3std', 'M+3std'])

    # 第三
    listsa, list_b = [], []

    data_na = data.fillna(0)
    for i in list(data_na):
        if len(list(set(data_na[i]))) <= number:
            list_b.append(i)
    for b in list_b:

        listda, sumx, lista = [], [], []

        lists = list(set(data_na[b]))
        for i in list(set(data_na[b])):
            lista.append((data_na[b] == i).sum())
        for i in lista:
            sumx.append(str("%.0f" % ((i / sum(lista)) * 100) + '%'))
        a = 0
        for x in lists:
            listda.append(str(x) + '(' + sumx[a] + ')')
            a += 1

        listsa.append(listda)
        listsa.append(lista)
    x = []
    for b in list_b:
        x.append(b)
        x.append(' ')
    df2 = pd.DataFrame(data=listsa, index=x)

# 打印模块
    if save:
        writer = pd.ExcelWriter('数据质量.xlsx')
        df1.to_excel(writer, '空值')
        df2.to_excel(writer, '类别')
        df3.to_excel(writer, '数值')
        writer.save()
    else:
        pass

    if df == 2:
        return df2
    elif df == 3:
        return df3
    else:
        return df1


def contrast_merge(data1, data1_name, data2, data2_sta_name, data2_end_name, data2_key_name, how="left"):
    """
    :param data1: 需要比较的数据源
    :param data1_name: 需要比较的列名称
    :param data2: 比较数据源
    :param data2_sta_name: 比较区间开始列的名称
    :param data2_end_name: 比较区间结束列的名称
    :param data2_key_name: data2 的主键
    :param how: 表链接方式  how有5个参数left,right,outer,inner,cross，具体参考marge中的how参数
    :return: 返回一个两张表链接的DateFrame
    注：涉及的名称需要字符串格式

    实例：
    st_en(data1=data_order, data1_name="shop_time", data2=data_promo, data2_sta_name="promo_start_date",
      data2_end_name="promo_end_date",data2_pr_key="promo_id")
    """
    import pandas as pd
    import numpy as np
    pr_key = data2[data2_key_name]
    sta = data2[data2_sta_name]
    end = data2[data2_end_name]
    da = data1[data1_name]
    for_1, for_2, for_3, for_4 = [], [], [], []

    for i in da:
        for j in range(len(sta)):
            if sta[j] <= i <= end[j]:
                for_1.append(j + 1)
            else:
                for_1.append(0)

    for i in list(range(len(da))):
        for_2.append(for_1[i * len(sta):(i + 1) * len(sta):])

    for i in range(len(da)):
        for_2[i].sort()
        for_3.append(max(for_2[i]) - 1)
        # print(x[i][-2])
    for i in for_3:
        if i < 0:
            for_4.append(np.nan)
        else:
            for_4.append(pr_key[i])
    data1[data2_key_name] = for_4

    data_or_pr = pd.merge(data1, data2, how=how, left_on=data2_key_name, right_on=data2_key_name)
    return data_or_pr
