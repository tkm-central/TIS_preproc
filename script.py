#coding:utf-8
import numpy as np
import pandas as pd

#データ読み込み
def import_data(filename):
	data_df= pd.read_csv(filename)
	return data_df

#データ書き出し
def export_data(df, filename):
	df.to_csv(filename, index=False, header=True)

#term属性を文字列から数値に変換
def term_to_num(df):
	f = lambda x: int(x.replace(" months", ""))
	df.term = list(map(f, list(df.term)))
	return df

#int_rate属性を数値に変換
def int_rate_to_num(df):
	f = lambda x: float(x.replace("%", ""))
	df.int_rate = list(map(f, list(df.int_rate)))
	return df

#emp_length属性を文字列に変換（nanは0扱い）
def emp_length_to_num(df):
	def f(x):
		if x=="n/a":
			return 0
		elif x=="10+ years":
			return 10
		elif x=="< 1 year":
			return 0
		elif x=="1 year":
			return 1
		else:
			return int(x.replace(" years", ""))
	df.emp_length = list(map(f, list(df.emp_length)))
	return df


#欠損値が多い（del_rate以上）属性をdrop
def drop_nullattr(df, del_rate):
	df_new = df
	for i in range(len(df.columns)):
	    attr = list(df.iloc[:, i])
	    name = df.iloc[:, i].name
	    count = 0
	    for item in attr:
	        if not item==item:
	            count = count+1
	    if(count>del_rate*len(df)):
	        print(name)
	        print("del")
	        df_new = df.drop(name, axis=1)
	return df_new


filename = "training_data.csv"
df = import_data(filename)

df = emp_length_to_num(df)
df = term_to_num(df)
df = int_rate_to_num(df)


# df = df.dropna(axis=1) #欠損値を含む列を削除
# df = df.drop(["zip_code", "emp_length"], axis=1) #emp_length列を削除（n/aを含むので），関係なさそうな列を削除


df = drop_nullattr(df, 0.1)
# df = df.loc[:, ["id", "grade", "home_ownership", "sub_grade", "int_rate", "mort_acc",  "is_good_customer"]]
print(len(df.columns))




export_data(df, "test2_train.csv")



