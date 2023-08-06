def mysql(sql, root, password, host, db):

    from sqlalchemy import create_engine
    import pandas as pd
    from string import Template

    # 初始化引擎
    engine = create_engine('mysql+pymysql://{0}:{1}@{2}/{3}'.format(root,password,host,db))
    query_sql = sql
    query_sql = Template(query_sql)  # template方法

    df = pd.read_sql_query(query_sql.substitute(), engine)  # 配合pandas的方法读取数据库值
    # 配合pandas的to_sql方法使用十分方便（dataframe对象直接入库）
    return df
