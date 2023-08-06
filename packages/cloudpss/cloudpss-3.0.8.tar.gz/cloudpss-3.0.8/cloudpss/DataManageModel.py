class DataManageModel(object):
    def GetDataItem(id: str):
        '''
            获取itemID对应的元素信息
            
            :params: itemID string类型，代表数据项的标识符，可以在所有类型的数据项中实现唯一标识
            
            :return: dict类型，为源数据的引用，返回该数据项的信息
        '''

    def GetItemIDList(dataType: str):
        '''
            获取dataType类型对应所有数据项的itemID列表
            
            :params: dataType enum类型，数据的种类标识，比如Transformer, Load, HeatPrice等等
            
            :return: list类型，返回该种类下所有数据项的itemID的列表
        '''

        pass

    def AddDataItem(dataType, data):
        '''
            向dataType类型的数据库中添加内容为data的数据项
            
            :params: dataType enum类型，数据的种类标识，比如Transformer, Load, HeatPrice等等
            :params: data dict类型，表示添加的数据内容，其数据结构应满足对应数据项的结构要求
            
            :return: string类型，返回新添加数据项的itemID，如果数据结构不满足要求，应当抛出异常
        '''
        pass

    def SetProjectPosition(longitude, latitude):
        '''
            将项目的经纬度位置坐标设置为(longitude, latitude)
            
            :params: longitude float类型，表示经度，范围为气象数据源的经度范围
            :params: latitude float类型，表示纬度，范围为气象数据源的纬度范围
        '''
        pass

    def GetAtmosData(startDate, endDate):
        '''
            获取在startDate到endDate之间的气象数据
            
            :params: startDate dateTime类型，表示开始时间
            :params: endDate dateTime类型，表示结束时间
            
            :return: list<dict>类型，为源数据的引用，返回当前项目位置对应时间范围内的气象数据序列，每个元素用字典进行表示，字典的key即区分不同的气象数据项（如风速、太阳辐照等）以及标识当前时间点
        '''
        pass