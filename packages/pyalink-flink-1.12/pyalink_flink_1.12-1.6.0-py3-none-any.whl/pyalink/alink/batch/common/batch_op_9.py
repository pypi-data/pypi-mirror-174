# -*- coding: utf-8 -*-

from ..base import BatchOperator, BaseSinkBatchOp
from ..mixins import WithTrainInfo, EvaluationMetricsCollector, ExtractModelInfoBatchOp, WithModelInfoBatchOp



class VectorBiFunctionBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorBiFunctionBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorBiFunctionBatchOp, self).__init__(*args, **kwargs)
        pass

    def setBiFuncName(self, val):
        return self._add_param('biFuncName', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class VectorChiSqSelectorBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.VectorChiSqSelectorBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorChiSqSelectorBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setFdr(self, val):
        return self._add_param('fdr', val)

    def setFpr(self, val):
        return self._add_param('fpr', val)

    def setFwe(self, val):
        return self._add_param('fwe', val)

    def setNumTopFeatures(self, val):
        return self._add_param('numTopFeatures', val)

    def setPercentile(self, val):
        return self._add_param('percentile', val)

    def setSelectorType(self, val):
        return self._add_param('selectorType', val)



class VectorChiSquareTestBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.statistics.VectorChiSquareTestBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorChiSquareTestBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)



class VectorCorrelationBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.statistics.VectorCorrelationBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorCorrelationBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setMethod(self, val):
        return self._add_param('method', val)



class VectorElementwiseProductBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorElementwiseProductBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorElementwiseProductBatchOp, self).__init__(*args, **kwargs)
        pass

    def setScalingVector(self, val):
        return self._add_param('scalingVector', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class VectorFunctionBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorFunctionBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorFunctionBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFuncName(self, val):
        return self._add_param('funcName', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setWithVariable(self, val):
        return self._add_param('WithVariable', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class VectorImputerModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorImputerModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorImputerModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass



class VectorImputerPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorImputerPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorImputerPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)



class VectorImputerTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorImputerTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorImputerTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setFillValue(self, val):
        return self._add_param('fillValue', val)

    def setStrategy(self, val):
        return self._add_param('strategy', val)



class VectorInteractionBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorInteractionBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorInteractionBatchOp, self).__init__(*args, **kwargs)
        pass

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class VectorMaxAbsScalerModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorMaxAbsScalerModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorMaxAbsScalerModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass



class VectorMaxAbsScalerPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorMaxAbsScalerPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorMaxAbsScalerPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)



class VectorMaxAbsScalerTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorMaxAbsScalerTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorMaxAbsScalerTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)



class VectorMinMaxScalerModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorMinMaxScalerModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorMinMaxScalerModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass



class VectorMinMaxScalerPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorMinMaxScalerPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorMinMaxScalerPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)



class VectorMinMaxScalerTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorMinMaxScalerTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorMinMaxScalerTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setMax(self, val):
        return self._add_param('max', val)

    def setMin(self, val):
        return self._add_param('min', val)



class VectorNearestNeighborPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.similarity.VectorNearestNeighborPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorNearestNeighborPredictBatchOp, self).__init__(*args, **kwargs)
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



class VectorNearestNeighborTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.similarity.VectorNearestNeighborTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorNearestNeighborTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setIdCol(self, val):
        return self._add_param('idCol', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setTrainType(self, val):
        return self._add_param('trainType', val)

    def setMetric(self, val):
        return self._add_param('metric', val)



class VectorNormalizeBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorNormalizeBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorNormalizeBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setP(self, val):
        return self._add_param('p', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class VectorPolynomialExpandBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorPolynomialExpandBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorPolynomialExpandBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setDegree(self, val):
        return self._add_param('degree', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class VectorPredict(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.common.tree.Preprocessing$VectorPredict'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorPredict, self).__init__(*args, **kwargs)
        pass

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setDropLast(self, val):
        return self._add_param('dropLast', val)

    def setEncode(self, val):
        return self._add_param('encode', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class VectorSizeHintBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorSizeHintBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorSizeHintBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setSize(self, val):
        return self._add_param('size', val)

    def setHandleInvalidMethod(self, val):
        return self._add_param('handleInvalidMethod', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class VectorSliceBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorSliceBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorSliceBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setIndices(self, val):
        return self._add_param('indices', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class VectorStandardScalerModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorStandardScalerModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorStandardScalerModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass



class VectorStandardScalerPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorStandardScalerPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorStandardScalerPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)



class VectorStandardScalerTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.vector.VectorStandardScalerTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorStandardScalerTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setWithMean(self, val):
        return self._add_param('withMean', val)

    def setWithStd(self, val):
        return self._add_param('withStd', val)



class VectorSummarizerBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.statistics.VectorSummarizerBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorSummarizerBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)



class VectorToColumnsBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.VectorToColumnsBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorToColumnsBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class VectorToCsvBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.VectorToCsvBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorToCsvBatchOp, self).__init__(*args, **kwargs)
        pass

    def setCsvCol(self, val):
        return self._add_param('csvCol', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setCsvFieldDelimiter(self, val):
        return self._add_param('csvFieldDelimiter', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setQuoteChar(self, val):
        return self._add_param('quoteChar', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class VectorToJsonBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.VectorToJsonBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorToJsonBatchOp, self).__init__(*args, **kwargs)
        pass

    def setJsonCol(self, val):
        return self._add_param('jsonCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class VectorToKvBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.VectorToKvBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorToKvBatchOp, self).__init__(*args, **kwargs)
        pass

    def setKvCol(self, val):
        return self._add_param('kvCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setKvColDelimiter(self, val):
        return self._add_param('kvColDelimiter', val)

    def setKvValDelimiter(self, val):
        return self._add_param('kvValDelimiter', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class VectorToTensorBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.VectorToTensorBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorToTensorBatchOp, self).__init__(*args, **kwargs)
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



class VectorToTripleBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.format.VectorToTripleBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorToTripleBatchOp, self).__init__(*args, **kwargs)
        pass

    def setTripleColumnValueSchemaStr(self, val):
        return self._add_param('tripleColumnValueSchemaStr', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class VectorTrain(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.common.tree.Preprocessing$VectorTrain'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VectorTrain, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setLeftOpen(self, val):
        return self._add_param('leftOpen', val)

    def setNumBuckets(self, val):
        return self._add_param('numBuckets', val)

    def setNumBucketsArray(self, val):
        return self._add_param('numBucketsArray', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class VertexClusterCoefficientBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.graph.VertexClusterCoefficientBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(VertexClusterCoefficientBatchOp, self).__init__(*args, **kwargs)
        pass

    def setEdgeSourceCol(self, val):
        return self._add_param('edgeSourceCol', val)

    def setEdgeTargetCol(self, val):
        return self._add_param('edgeTargetCol', val)

    def setAsUndirectedGraph(self, val):
        return self._add_param('asUndirectedGraph', val)



class WeightSampleBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.WeightSampleBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(WeightSampleBatchOp, self).__init__(*args, **kwargs)
        pass

    def setRatio(self, val):
        return self._add_param('ratio', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setWithReplacement(self, val):
        return self._add_param('withReplacement', val)



class WhereBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sql.WhereBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(WhereBatchOp, self).__init__(*args, **kwargs)
        pass

    def setClause(self, val):
        return self._add_param('clause', val)



class Word2VecPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.nlp.Word2VecPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(Word2VecPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setPredMethod(self, val):
        return self._add_param('predMethod', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setWordDelimiter(self, val):
        return self._add_param('wordDelimiter', val)



class Word2VecTrainBatchOp(BatchOperator, WithTrainInfo):
    CLS_NAME = 'com.alibaba.alink.operator.batch.nlp.Word2VecTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(Word2VecTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setAlpha(self, val):
        return self._add_param('alpha', val)

    def setMinCount(self, val):
        return self._add_param('minCount', val)

    def setNumIter(self, val):
        return self._add_param('numIter', val)

    def setRandomWindow(self, val):
        return self._add_param('randomWindow', val)

    def setVectorSize(self, val):
        return self._add_param('vectorSize', val)

    def setWindow(self, val):
        return self._add_param('window', val)

    def setWordDelimiter(self, val):
        return self._add_param('wordDelimiter', val)



class WordCountBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.nlp.WordCountBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(WordCountBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setWordDelimiter(self, val):
        return self._add_param('wordDelimiter', val)



class WriteTensorToImageBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.image.WriteTensorToImageBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(WriteTensorToImageBatchOp, self).__init__(*args, **kwargs)
        pass

    def setRelativeFilePathCol(self, val):
        return self._add_param('relativeFilePathCol', val)

    def setRootFilePath(self, val):
        return self._add_param('rootFilePath', val)

    def setTensorCol(self, val):
        return self._add_param('tensorCol', val)

    def setImageType(self, val):
        return self._add_param('imageType', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class XGBoostPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.XGBoostPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(XGBoostPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPluginVersion(self, val):
        return self._add_param('pluginVersion', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class XGBoostRegPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.XGBoostRegPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(XGBoostRegPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPluginVersion(self, val):
        return self._add_param('pluginVersion', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class XGBoostRegTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.XGBoostRegTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(XGBoostRegTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setNumRound(self, val):
        return self._add_param('numRound', val)

    def setAlpha(self, val):
        return self._add_param('alpha', val)

    def setBaseScore(self, val):
        return self._add_param('baseScore', val)

    def setColSampleByLevel(self, val):
        return self._add_param('colSampleByLevel', val)

    def setColSampleByNode(self, val):
        return self._add_param('colSampleByNode', val)

    def setColSampleByTree(self, val):
        return self._add_param('colSampleByTree', val)

    def setEta(self, val):
        return self._add_param('eta', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setGamma(self, val):
        return self._add_param('gamma', val)

    def setGrowPolicy(self, val):
        return self._add_param('growPolicy', val)

    def setInteractionConstraints(self, val):
        return self._add_param('interactionConstraints', val)

    def setLambda(self, val):
        return self._add_param('lambda', val)

    def setMaxBin(self, val):
        return self._add_param('maxBin', val)

    def setMaxDeltaStep(self, val):
        return self._add_param('maxDeltaStep', val)

    def setMaxDepth(self, val):
        return self._add_param('maxDepth', val)

    def setMaxLeaves(self, val):
        return self._add_param('maxLeaves', val)

    def setMinChildWeight(self, val):
        return self._add_param('minChildWeight', val)

    def setMonotoneConstraints(self, val):
        return self._add_param('monotoneConstraints', val)

    def setNumClass(self, val):
        return self._add_param('numClass', val)

    def setObjective(self, val):
        return self._add_param('objective', val)

    def setPluginVersion(self, val):
        return self._add_param('pluginVersion', val)

    def setProcessType(self, val):
        return self._add_param('processType', val)

    def setRefreshLeaf(self, val):
        return self._add_param('refreshLeaf', val)

    def setRunningMode(self, val):
        return self._add_param('runningMode', val)

    def setSamplingMethod(self, val):
        return self._add_param('samplingMethod', val)

    def setScalePosWeight(self, val):
        return self._add_param('scalePosWeight', val)

    def setSinglePrecisionHistogram(self, val):
        return self._add_param('singlePrecisionHistogram', val)

    def setSketchEps(self, val):
        return self._add_param('sketchEps', val)

    def setSubSample(self, val):
        return self._add_param('subSample', val)

    def setTreeMethod(self, val):
        return self._add_param('treeMethod', val)

    def setTweedieVariancePower(self, val):
        return self._add_param('tweedieVariancePower', val)

    def setUpdater(self, val):
        return self._add_param('updater', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class XGBoostTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.XGBoostTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(XGBoostTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setNumRound(self, val):
        return self._add_param('numRound', val)

    def setAlpha(self, val):
        return self._add_param('alpha', val)

    def setBaseScore(self, val):
        return self._add_param('baseScore', val)

    def setColSampleByLevel(self, val):
        return self._add_param('colSampleByLevel', val)

    def setColSampleByNode(self, val):
        return self._add_param('colSampleByNode', val)

    def setColSampleByTree(self, val):
        return self._add_param('colSampleByTree', val)

    def setEta(self, val):
        return self._add_param('eta', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setGamma(self, val):
        return self._add_param('gamma', val)

    def setGrowPolicy(self, val):
        return self._add_param('growPolicy', val)

    def setInteractionConstraints(self, val):
        return self._add_param('interactionConstraints', val)

    def setLambda(self, val):
        return self._add_param('lambda', val)

    def setMaxBin(self, val):
        return self._add_param('maxBin', val)

    def setMaxDeltaStep(self, val):
        return self._add_param('maxDeltaStep', val)

    def setMaxDepth(self, val):
        return self._add_param('maxDepth', val)

    def setMaxLeaves(self, val):
        return self._add_param('maxLeaves', val)

    def setMinChildWeight(self, val):
        return self._add_param('minChildWeight', val)

    def setMonotoneConstraints(self, val):
        return self._add_param('monotoneConstraints', val)

    def setNumClass(self, val):
        return self._add_param('numClass', val)

    def setObjective(self, val):
        return self._add_param('objective', val)

    def setPluginVersion(self, val):
        return self._add_param('pluginVersion', val)

    def setProcessType(self, val):
        return self._add_param('processType', val)

    def setRefreshLeaf(self, val):
        return self._add_param('refreshLeaf', val)

    def setRunningMode(self, val):
        return self._add_param('runningMode', val)

    def setSamplingMethod(self, val):
        return self._add_param('samplingMethod', val)

    def setScalePosWeight(self, val):
        return self._add_param('scalePosWeight', val)

    def setSinglePrecisionHistogram(self, val):
        return self._add_param('singlePrecisionHistogram', val)

    def setSketchEps(self, val):
        return self._add_param('sketchEps', val)

    def setSubSample(self, val):
        return self._add_param('subSample', val)

    def setTreeMethod(self, val):
        return self._add_param('treeMethod', val)

    def setUpdater(self, val):
        return self._add_param('updater', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class XlsSourceBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.source.XlsSourceBatchOp'
    OP_TYPE = 'SOURCE'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(XlsSourceBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFilePath(self, val):
        return self._add_param('filePath', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setIgnoreFirstLine(self, val):
        return self._add_param('ignoreFirstLine', val)

    def setSheetId(self, val):
        return self._add_param('sheetId', val)



class Zipped2KObjectBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.common.recommendation.Zipped2KObjectBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(Zipped2KObjectBatchOp, self).__init__(*args, **kwargs)
        pass

    def setGroupCol(self, val):
        return self._add_param('groupCol', val)

    def setObjectCol(self, val):
        return self._add_param('objectCol', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setInfoCols(self, val):
        return self._add_param('infoCols', val)

