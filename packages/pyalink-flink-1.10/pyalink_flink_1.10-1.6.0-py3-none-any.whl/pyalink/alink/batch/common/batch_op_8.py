# -*- coding: utf-8 -*-

from ..base import BatchOperator, BaseSinkBatchOp
from ..mixins import WithTrainInfo, EvaluationMetricsCollector, ExtractModelInfoBatchOp, WithModelInfoBatchOp



class StringNearestNeighborTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.similarity.StringNearestNeighborTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(StringNearestNeighborTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setIdCol(self, val):
        return self._add_param('idCol', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setTrainType(self, val):
        return self._add_param('trainType', val)

    def setLambda(self, val):
        return self._add_param('lambda', val)

    def setMetric(self, val):
        return self._add_param('metric', val)

    def setWindowSize(self, val):
        return self._add_param('windowSize', val)



class StringSimilarityPairwiseBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.similarity.StringSimilarityPairwiseBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(StringSimilarityPairwiseBatchOp, self).__init__(*args, **kwargs)
        pass

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setLambda(self, val):
        return self._add_param('lambda', val)

    def setMetric(self, val):
        return self._add_param('metric', val)

    def setNumBucket(self, val):
        return self._add_param('numBucket', val)

    def setNumHashTables(self, val):
        return self._add_param('numHashTables', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSeed(self, val):
        return self._add_param('seed', val)

    def setWindowSize(self, val):
        return self._add_param('windowSize', val)



class SummarizerBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.statistics.SummarizerBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(SummarizerBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)



class SwingRecommBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.SwingRecommBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(SwingRecommBatchOp, self).__init__(*args, **kwargs)
        pass

    def setItemCol(self, val):
        return self._add_param('itemCol', val)

    def setRecommCol(self, val):
        return self._add_param('recommCol', val)

    def setInitRecommCol(self, val):
        return self._add_param('initRecommCol', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class SwingTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.SwingTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(SwingTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setItemCol(self, val):
        return self._add_param('itemCol', val)

    def setUserCol(self, val):
        return self._add_param('userCol', val)

    def setAlpha(self, val):
        return self._add_param('alpha', val)

    def setMaxItemNumber(self, val):
        return self._add_param('maxItemNumber', val)

    def setMaxUserItems(self, val):
        return self._add_param('maxUserItems', val)

    def setMinUserItems(self, val):
        return self._add_param('minUserItems', val)

    def setResultNormalize(self, val):
        return self._add_param('resultNormalize', val)

    def setUserAlpha(self, val):
        return self._add_param('userAlpha', val)

    def setUserBeta(self, val):
        return self._add_param('userBeta', val)



class TF2TableModelTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.tensorflow.TF2TableModelTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TF2TableModelTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setMainScriptFile(self, val):
        return self._add_param('mainScriptFile', val)

    def setUserFiles(self, val):
        return self._add_param('userFiles', val)

    def setIntraOpParallelism(self, val):
        return self._add_param('intraOpParallelism', val)

    def setNumPSs(self, val):
        return self._add_param('numPSs', val)

    def setNumWorkers(self, val):
        return self._add_param('numWorkers', val)

    def setPythonEnv(self, val):
        return self._add_param('pythonEnv', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setUserParams(self, val):
        return self._add_param('userParams', val)



class TFRecordDatasetSinkBatchOp(BaseSinkBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sink.TFRecordDatasetSinkBatchOp'
    OP_TYPE = 'SINK'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TFRecordDatasetSinkBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFilePath(self, val):
        return self._add_param('filePath', val)

    def setNumFiles(self, val):
        return self._add_param('numFiles', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)



class TFRecordDatasetSourceBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.source.TFRecordDatasetSourceBatchOp'
    OP_TYPE = 'SOURCE'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TFRecordDatasetSourceBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFilePath(self, val):
        return self._add_param('filePath', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)



class TFSavedModelPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.tensorflow.TFSavedModelPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TFSavedModelPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setModelPath(self, val):
        return self._add_param('modelPath', val)

    def setOutputSchemaStr(self, val):
        return self._add_param('outputSchemaStr', val)

    def setGraphDefTag(self, val):
        return self._add_param('graphDefTag', val)

    def setInputSignatureDefs(self, val):
        return self._add_param('inputSignatureDefs', val)

    def setIntraOpParallelism(self, val):
        return self._add_param('intraOpParallelism', val)

    def setOutputSignatureDefs(self, val):
        return self._add_param('outputSignatureDefs', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setSignatureDefKey(self, val):
        return self._add_param('signatureDefKey', val)



class TFTableModelPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.tensorflow.TFTableModelPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TFTableModelPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setOutputSchemaStr(self, val):
        return self._add_param('outputSchemaStr', val)

    def setGraphDefTag(self, val):
        return self._add_param('graphDefTag', val)

    def setInputSignatureDefs(self, val):
        return self._add_param('inputSignatureDefs', val)

    def setIntraOpParallelism(self, val):
        return self._add_param('intraOpParallelism', val)

    def setOutputSignatureDefs(self, val):
        return self._add_param('outputSignatureDefs', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setSignatureDefKey(self, val):
        return self._add_param('signatureDefKey', val)



class TFTableModelTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.tensorflow.TFTableModelTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TFTableModelTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setMainScriptFile(self, val):
        return self._add_param('mainScriptFile', val)

    def setUserFiles(self, val):
        return self._add_param('userFiles', val)

    def setIntraOpParallelism(self, val):
        return self._add_param('intraOpParallelism', val)

    def setNumPSs(self, val):
        return self._add_param('numPSs', val)

    def setNumWorkers(self, val):
        return self._add_param('numWorkers', val)

    def setPythonEnv(self, val):
        return self._add_param('pythonEnv', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setUserParams(self, val):
        return self._add_param('userParams', val)



class TensorFlow2BatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.tensorflow.TensorFlow2BatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TensorFlow2BatchOp, self).__init__(*args, **kwargs)
        pass

    def setMainScriptFile(self, val):
        return self._add_param('mainScriptFile', val)

    def setOutputSchemaStr(self, val):
        return self._add_param('outputSchemaStr', val)

    def setUserFiles(self, val):
        return self._add_param('userFiles', val)

    def setIntraOpParallelism(self, val):
        return self._add_param('intraOpParallelism', val)

    def setNumPSs(self, val):
        return self._add_param('numPSs', val)

    def setNumWorkers(self, val):
        return self._add_param('numWorkers', val)

    def setPythonEnv(self, val):
        return self._add_param('pythonEnv', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setUserParams(self, val):
        return self._add_param('userParams', val)



class TensorFlowBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.tensorflow.TensorFlowBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TensorFlowBatchOp, self).__init__(*args, **kwargs)
        pass

    def setMainScriptFile(self, val):
        return self._add_param('mainScriptFile', val)

    def setOutputSchemaStr(self, val):
        return self._add_param('outputSchemaStr', val)

    def setUserFiles(self, val):
        return self._add_param('userFiles', val)

    def setIntraOpParallelism(self, val):
        return self._add_param('intraOpParallelism', val)

    def setNumPSs(self, val):
        return self._add_param('numPSs', val)

    def setNumWorkers(self, val):
        return self._add_param('numWorkers', val)

    def setPythonEnv(self, val):
        return self._add_param('pythonEnv', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setUserParams(self, val):
        return self._add_param('userParams', val)



class TensorReshapeBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.tensor.TensorReshapeBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TensorReshapeBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setSize(self, val):
        return self._add_param('size', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class TensorToVectorBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.TensorToVectorBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TensorToVectorBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setConvertMethod(self, val):
        return self._add_param('convertMethod', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class TextApproxNearestNeighborPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.similarity.TextApproxNearestNeighborPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TextApproxNearestNeighborPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setRadius(self, val):
        return self._add_param('radius', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setTopN(self, val):
        return self._add_param('topN', val)



class TextApproxNearestNeighborTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.similarity.TextApproxNearestNeighborTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TextApproxNearestNeighborTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setIdCol(self, val):
        return self._add_param('idCol', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setTrainType(self, val):
        return self._add_param('trainType', val)

    def setMetric(self, val):
        return self._add_param('metric', val)

    def setNumBucket(self, val):
        return self._add_param('numBucket', val)

    def setNumHashTables(self, val):
        return self._add_param('numHashTables', val)

    def setSeed(self, val):
        return self._add_param('seed', val)



class TextNearestNeighborPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.similarity.TextNearestNeighborPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TextNearestNeighborPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setRadius(self, val):
        return self._add_param('radius', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setTopN(self, val):
        return self._add_param('topN', val)



class TextNearestNeighborTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.similarity.TextNearestNeighborTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TextNearestNeighborTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setIdCol(self, val):
        return self._add_param('idCol', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setTrainType(self, val):
        return self._add_param('trainType', val)

    def setLambda(self, val):
        return self._add_param('lambda', val)

    def setMetric(self, val):
        return self._add_param('metric', val)

    def setWindowSize(self, val):
        return self._add_param('windowSize', val)



class TextSimilarityPairwiseBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.similarity.TextSimilarityPairwiseBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TextSimilarityPairwiseBatchOp, self).__init__(*args, **kwargs)
        pass

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setLambda(self, val):
        return self._add_param('lambda', val)

    def setMetric(self, val):
        return self._add_param('metric', val)

    def setNumBucket(self, val):
        return self._add_param('numBucket', val)

    def setNumHashTables(self, val):
        return self._add_param('numHashTables', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSeed(self, val):
        return self._add_param('seed', val)

    def setWindowSize(self, val):
        return self._add_param('windowSize', val)



class TextSinkBatchOp(BaseSinkBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sink.TextSinkBatchOp'
    OP_TYPE = 'SINK'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TextSinkBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFilePath(self, val):
        return self._add_param('filePath', val)

    def setNumFiles(self, val):
        return self._add_param('numFiles', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setPartitionCols(self, val):
        return self._add_param('partitionCols', val)



class TextSourceBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.source.TextSourceBatchOp'
    OP_TYPE = 'SOURCE'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TextSourceBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFilePath(self, val):
        return self._add_param('filePath', val)

    def setIgnoreFirstLine(self, val):
        return self._add_param('ignoreFirstLine', val)

    def setPartitions(self, val):
        return self._add_param('partitions', val)

    def setTextCol(self, val):
        return self._add_param('textCol', val)



class TfidfBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.nlp.TfidfBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TfidfBatchOp, self).__init__(*args, **kwargs)
        pass

    def setCountCol(self, val):
        return self._add_param('countCol', val)

    def setDocIdCol(self, val):
        return self._add_param('docIdCol', val)

    def setWordCol(self, val):
        return self._add_param('wordCol', val)



class ToMTableBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.ToMTableBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ToMTableBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setHandleInvalidMethod(self, val):
        return self._add_param('handleInvalidMethod', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class ToTensorBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.ToTensorBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ToTensorBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setHandleInvalidMethod(self, val):
        return self._add_param('handleInvalidMethod', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setTensorDataType(self, val):
        return self._add_param('tensorDataType', val)

    def setTensorShape(self, val):
        return self._add_param('tensorShape', val)



class ToVectorBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.ToVectorBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ToVectorBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setHandleInvalidMethod(self, val):
        return self._add_param('handleInvalidMethod', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorType(self, val):
        return self._add_param('vectorType', val)



class TokenizerBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.nlp.TokenizerBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TokenizerBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class TorchModelPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.pytorch.TorchModelPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TorchModelPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setModelPath(self, val):
        return self._add_param('modelPath', val)

    def setOutputSchemaStr(self, val):
        return self._add_param('outputSchemaStr', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setIntraOpParallelism(self, val):
        return self._add_param('intraOpParallelism', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class TreeDepthBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.graph.TreeDepthBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TreeDepthBatchOp, self).__init__(*args, **kwargs)
        pass

    def setEdgeSourceCol(self, val):
        return self._add_param('edgeSourceCol', val)

    def setEdgeTargetCol(self, val):
        return self._add_param('edgeTargetCol', val)

    def setAsUndirectedGraph(self, val):
        return self._add_param('asUndirectedGraph', val)

    def setEdgeWeightCol(self, val):
        return self._add_param('edgeWeightCol', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)



class TreeModelEncoderBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.TreeModelEncoderBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TreeModelEncoderBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class TriangleListBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.graph.TriangleListBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TriangleListBatchOp, self).__init__(*args, **kwargs)
        pass

    def setEdgeSourceCol(self, val):
        return self._add_param('edgeSourceCol', val)

    def setEdgeTargetCol(self, val):
        return self._add_param('edgeTargetCol', val)



class TripleToColumnsBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.TripleToColumnsBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TripleToColumnsBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setTripleColumnCol(self, val):
        return self._add_param('tripleColumnCol', val)

    def setTripleValueCol(self, val):
        return self._add_param('tripleValueCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setTripleRowCol(self, val):
        return self._add_param('tripleRowCol', val)



class TripleToCsvBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.TripleToCsvBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TripleToCsvBatchOp, self).__init__(*args, **kwargs)
        pass

    def setCsvCol(self, val):
        return self._add_param('csvCol', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setTripleColumnCol(self, val):
        return self._add_param('tripleColumnCol', val)

    def setTripleValueCol(self, val):
        return self._add_param('tripleValueCol', val)

    def setCsvFieldDelimiter(self, val):
        return self._add_param('csvFieldDelimiter', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setQuoteChar(self, val):
        return self._add_param('quoteChar', val)

    def setTripleRowCol(self, val):
        return self._add_param('tripleRowCol', val)



class TripleToJsonBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.TripleToJsonBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TripleToJsonBatchOp, self).__init__(*args, **kwargs)
        pass

    def setJsonCol(self, val):
        return self._add_param('jsonCol', val)

    def setTripleColumnCol(self, val):
        return self._add_param('tripleColumnCol', val)

    def setTripleValueCol(self, val):
        return self._add_param('tripleValueCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setTripleRowCol(self, val):
        return self._add_param('tripleRowCol', val)



class TripleToKvBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.TripleToKvBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TripleToKvBatchOp, self).__init__(*args, **kwargs)
        pass

    def setKvCol(self, val):
        return self._add_param('kvCol', val)

    def setTripleColumnCol(self, val):
        return self._add_param('tripleColumnCol', val)

    def setTripleValueCol(self, val):
        return self._add_param('tripleValueCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setKvColDelimiter(self, val):
        return self._add_param('kvColDelimiter', val)

    def setKvValDelimiter(self, val):
        return self._add_param('kvValDelimiter', val)

    def setTripleRowCol(self, val):
        return self._add_param('tripleRowCol', val)



class TripleToVectorBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.TripleToVectorBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TripleToVectorBatchOp, self).__init__(*args, **kwargs)
        pass

    def setTripleColumnCol(self, val):
        return self._add_param('tripleColumnCol', val)

    def setTripleValueCol(self, val):
        return self._add_param('tripleValueCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setTripleRowCol(self, val):
        return self._add_param('tripleRowCol', val)

    def setVectorSize(self, val):
        return self._add_param('vectorSize', val)



class TsvSinkBatchOp(BaseSinkBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sink.TsvSinkBatchOp'
    OP_TYPE = 'SINK'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TsvSinkBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFilePath(self, val):
        return self._add_param('filePath', val)

    def setNumFiles(self, val):
        return self._add_param('numFiles', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setPartitionCols(self, val):
        return self._add_param('partitionCols', val)



class TsvSourceBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.source.TsvSourceBatchOp'
    OP_TYPE = 'SOURCE'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TsvSourceBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFilePath(self, val):
        return self._add_param('filePath', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setIgnoreFirstLine(self, val):
        return self._add_param('ignoreFirstLine', val)

    def setPartitions(self, val):
        return self._add_param('partitions', val)

    def setSkipBlankLine(self, val):
        return self._add_param('skipBlankLine', val)



class TypeConvertBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.TypeConvertBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(TypeConvertBatchOp, self).__init__(*args, **kwargs)
        pass

    def setTargetType(self, val):
        return self._add_param('targetType', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)



class UnionAllBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sql.UnionAllBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(UnionAllBatchOp, self).__init__(*args, **kwargs)
        pass



class UnionBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sql.UnionBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(UnionBatchOp, self).__init__(*args, **kwargs)
        pass



class UserCfItemsPerUserRecommBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.UserCfItemsPerUserRecommBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(UserCfItemsPerUserRecommBatchOp, self).__init__(*args, **kwargs)
        pass

    def setRecommCol(self, val):
        return self._add_param('recommCol', val)

    def setUserCol(self, val):
        return self._add_param('userCol', val)

    def setExcludeKnown(self, val):
        return self._add_param('excludeKnown', val)

    def setInitRecommCol(self, val):
        return self._add_param('initRecommCol', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class UserCfModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.UserCfModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(UserCfModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass



class UserCfRateRecommBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.UserCfRateRecommBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(UserCfRateRecommBatchOp, self).__init__(*args, **kwargs)
        pass

    def setItemCol(self, val):
        return self._add_param('itemCol', val)

    def setRecommCol(self, val):
        return self._add_param('recommCol', val)

    def setUserCol(self, val):
        return self._add_param('userCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class UserCfSimilarUsersRecommBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.UserCfSimilarUsersRecommBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(UserCfSimilarUsersRecommBatchOp, self).__init__(*args, **kwargs)
        pass

    def setRecommCol(self, val):
        return self._add_param('recommCol', val)

    def setUserCol(self, val):
        return self._add_param('userCol', val)

    def setInitRecommCol(self, val):
        return self._add_param('initRecommCol', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class UserCfTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.UserCfTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(UserCfTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setItemCol(self, val):
        return self._add_param('itemCol', val)

    def setUserCol(self, val):
        return self._add_param('userCol', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setRateCol(self, val):
        return self._add_param('rateCol', val)

    def setSimilarityThreshold(self, val):
        return self._add_param('similarityThreshold', val)

    def setSimilarityType(self, val):
        return self._add_param('similarityType', val)



class UserCfUsersPerItemRecommBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.UserCfUsersPerItemRecommBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(UserCfUsersPerItemRecommBatchOp, self).__init__(*args, **kwargs)
        pass

    def setItemCol(self, val):
        return self._add_param('itemCol', val)

    def setRecommCol(self, val):
        return self._add_param('recommCol', val)

    def setExcludeKnown(self, val):
        return self._add_param('excludeKnown', val)

    def setInitRecommCol(self, val):
        return self._add_param('initRecommCol', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class VectorApproxNearestNeighborPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.similarity.VectorApproxNearestNeighborPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorApproxNearestNeighborPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setRadius(self, val):
        return self._add_param('radius', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setTopN(self, val):
        return self._add_param('topN', val)



class VectorApproxNearestNeighborTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.similarity.VectorApproxNearestNeighborTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorApproxNearestNeighborTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setIdCol(self, val):
        return self._add_param('idCol', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setTrainType(self, val):
        return self._add_param('trainType', val)

    def setMetric(self, val):
        return self._add_param('metric', val)

    def setNumHashTables(self, val):
        return self._add_param('numHashTables', val)

    def setNumProjectionsPerTable(self, val):
        return self._add_param('numProjectionsPerTable', val)

    def setProjectionWidth(self, val):
        return self._add_param('projectionWidth', val)

    def setSeed(self, val):
        return self._add_param('seed', val)

    def setSolver(self, val):
        return self._add_param('solver', val)



class VectorAssemblerBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorAssemblerBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorAssemblerBatchOp, self).__init__(*args, **kwargs)
        pass

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setHandleInvalidMethod(self, val):
        return self._add_param('handleInvalidMethod', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

