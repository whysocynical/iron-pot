from model import Model
from model import Model
from sklearn.datasets import load_iris
from sklearn.datasets import load_wine
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import accuracy_score,f1_score


class GradientBoosting(Model):

    #加载数据集
    def load_data(self, dataname):
        if dataname == "iris":
            datas = load_iris()
            x= datas.data
            y= datas.target

        elif dataname == "wine":
            datas = load_wine()
            #放入DataFrame中便于查看
            x= datas.data
            y= datas.target

        #数据标准化
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(x)
        return x, y, X_scaled

    #数据分割并训练
    #k折(k=6)
    def split_data_K_Fold(self, data, ObservationIndex):
        #加载数据
        x,y,X_scaled = self.load_data(data)
        #k折分割
        kfolds = KFold(n_splits=6)
        for train_index,test_index in kfolds.split(X_scaled):
            # 准备交叉验证的数据
            x_train_fold = X_scaled[train_index]
            y_train_fold = y[train_index]
            x_test_fold = X_scaled[test_index]
            y_test_fold = y[test_index]

            # 训练
            gbrt = self.train_data(x_train_fold,y_train_fold)

            #评估
            self.Evaluations(gbrt, x_test_fold, y_test_fold, ObservationIndex)
    
    #random
    def split_data_Random(self, data, size, ObservationIndex):
        #加载数据
        x,y,X_scaled = self.load_data(data)
        #random分割
        x_train, x_test, y_train, y_test = train_test_split(X_scaled, y, test_size=size, random_state=3)
        
        #训练
        gbrt=self.train_data(x_train, y_train)
        
        #评估
        self.Evaluations(gbrt, x_test, y_test, ObservationIndex)
    
    #训练模型
    def train_data(self, X_train, y_train):
        gbrt = GradientBoostingRegressor(max_depth=2, n_estimators=3, random_state=42)
        gbrtf = gbrt.fit(X_train,y_train)
        return gbrtf

    #评估模型
    def Evaluations(self, model, x_test, y_test, ObservationIndex):
        y_pred = model.predict(x_test)
        #数据转int
        predictions = [round(value) for value in y_pred]
        if ObservationIndex == "acc":
            AccuracyScore = accuracy_score(y_test,predictions)
            print('accuracy_score : ', AccuracyScore)
        elif ObservationIndex == "f1":
            F1Score = f1_score(y_test,predictions, average='micro')
            print('f1_score for micro : ', F1Score)

    #测试模型
    def test(self, dataname, method, size, ObservationIndex):
        print("GradientBoosting test:")
        
        if method == "kfold":
            self.split_data_K_Fold(dataname, ObservationIndex)
        
        elif method == "random":
            self.split_data_Random(dataname, size, ObservationIndex)

if __name__ == '__main__':
    # 1. 创建一个算法模型对象
    a = GradientBoosting()
    # 2. 调用模型对象的方法
    a.test("iris", "kfold", 0.5, "acc")
    a.test("iris", "random", 0.9, "acc")