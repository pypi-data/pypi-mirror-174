#qt5: https://doc.bccnsoft.com/docs/PyQt5/qml.html
#qt6: https://doc.qt.io/qtforpython/tutorials/qmlintegration/qmlintegration.html
#QML_IMPORT_NAME = "io.qt.textproperties"
#QML_IMPORT_MAJOR_VERSION = 1

from typing import Iterable
from .rea import pipeline, pipelines, stream, scopeCache
from PyQt5.QtCore import QObject, pyqtSlot, QThread
from PyQt5.QtQml import QJSValue, QQmlApplicationEngine, QQmlEngine, QJSValueIterator

qml_engine = None

class pipelineQML(pipeline):
    def __init__(self, aName: str):
        super().__init__(aName)

class qmlScopeCache(QObject):
    def __init__(self, aScope: scopeCache):
        super().__init__()
        self.m_scope = aScope
    
    @pyqtSlot(str, QJSValue, result = QObject)
    def cache(self, aName: str, aData: QJSValue) -> QObject:
        self.m_scope.cache(aName, aData.toVariant())
        return self

    @pyqtSlot(str, result = QJSValue)
    def data(self, aName: str) -> QJSValue:
        return QJSValue(self.m_scope.data(aName))

class qmlStream(QObject):
    def __init__(self, aStream: stream):
        super().__init__()
        self.__m_stream = aStream
    
    @pyqtSlot(QJSValue, result = QObject)
    def setData(self, aData: QJSValue) -> QObject:
        self.__m_stream.setData(aData.toVariant())
        return self

    @pyqtSlot(result = QObject)
    @pyqtSlot(bool, result = QObject)
    def scope(self, aNew: bool = False) -> QObject:
        ret = qmlScopeCache(self.__m_stream.scope(aNew))
        qml_engine.setObjectOwnership(ret, QQmlEngine.ObjectOwnership.JavaScriptOwnership)
        return ret

    @pyqtSlot(result = QJSValue)
    def data(self) -> QJSValue:
        return QJSValue(self.__m_stream.data())

    @pyqtSlot(result = str)
    def tag(self) -> str:
        return self.__m_stream.tag()

    @pyqtSlot(result = QObject)
    @pyqtSlot(str, result = QObject)
    def out(self, aTag: str = "") -> QObject:
        self.__m_stream.out(aTag)
        return self

    @pyqtSlot(QJSValue, result = QObject)
    @pyqtSlot(QJSValue, str, result = QObject)
    @pyqtSlot(QJSValue, str, str, result = QObject)
    def outs(self, aOut: QJSValue, aNext: str = "", aTag: str = "") -> QObject:
        ret = qmlStream(self.__m_stream.outs(aOut.toVariant(), aNext, aTag))
        qml_engine.setObjectOwnership(ret, QQmlEngine.ObjectOwnership.JavaScriptOwnership)
        return ret

    @pyqtSlot(QJSValue, result = QObject)
    @pyqtSlot(QJSValue, str, result = QObject)
    @pyqtSlot(QJSValue, str, str, result = QObject)
    def outsB(self, aOut: QJSValue, aNext: str = "", aTag: str = "") -> QObject:
        self.outs(aOut, aNext, aTag)
        return self
    
    @pyqtSlot()
    def noOut(self):
        self.__m_stream.noOut()

    @pyqtSlot(str, result = QObject)
    @pyqtSlot(str, bool, result = QObject)
    @pyqtSlot(str, bool, str, result = QObject)
    @pyqtSlot(str, bool, str, bool, result = QObject)
    def asyncCall(self, aName: str, aEventLevel: bool = True, aPipeline: str = "py_qml", aOutside: bool = False) -> QObject:
        ret = qmlStream(self.__m_stream.asyncCall(aName, aEventLevel, aPipeline, aOutside))
        qml_engine.setObjectOwnership(ret, QQmlEngine.ObjectOwnership.JavaScriptOwnership)
        return ret

    @pyqtSlot(QJSValue, result = QObject)
    @pyqtSlot(QJSValue, dict, result = QObject)
    @pyqtSlot(QJSValue, dict, bool, result = QObject)
    @pyqtSlot(QJSValue, dict, bool, str, result = QObject)
    def asyncCallF(self, aFunc: QJSValue, aParam: dict = {}, aEventLevel: bool = True, aPipeline: str = "py") -> QObject:
        f = QJSValue(aFunc)
        def func(aStream: stream):
            f.call([qml_engine.newQObject(qmlStream(aStream))])
        ret = qmlStream(self.__m_stream.asyncCallF(func, aParam, aEventLevel, aPipeline))
        qml_engine.setObjectOwnership(ret, QQmlEngine.ObjectOwnership.JavaScriptOwnership)
        return ret

class qmlPipe(QObject):
    def __init__(self, aParent: pipeline, aName: str):
        super().__init__()
        self.__m_parent = aParent
        self.__m_name = aName

    @pyqtSlot(result = str)
    def actName(self) -> str:
        return self.__m_name

    @pyqtSlot(str, result = QObject)
    @pyqtSlot(str, str, result = QObject)
    def next(self, aName: str, aTag: str = "") -> QObject:
        ret = qmlPipe(self.__m_parent, aName)
        self.__m_parent.find(self.__m_name).next(aName, aTag)
        qml_engine.setObjectOwnership(ret, QQmlEngine.ObjectOwnership.JavaScriptOwnership)
        return ret
    
    @pyqtSlot(str, result = QObject)
    @pyqtSlot(str, str, result = QObject)
    def nextB(self, aName: str, aTag: str = "") -> QObject:
        self.next(aName, aTag)
        return self

    @pyqtSlot(QJSValue, result = QObject)
    @pyqtSlot(QJSValue, str, result = QObject)
    @pyqtSlot(QJSValue, str, dict, result = QObject)
    def nextF(self, aFunc: QJSValue, aTag: str = "", aParam: dict = {}) -> QObject:
        f = QJSValue(aFunc)
        def func(aStream: stream):
            f.call([qml_engine.newQObject(qmlStream(aStream))])
        return self.next(self.__m_parent.add(func, aParam).actName(), aTag)

    @pyqtSlot(QJSValue, result = QObject)
    @pyqtSlot(QJSValue, str, result = QObject)
    @pyqtSlot(QJSValue, str, dict, result = QObject)
    def nextFB(self, aFunc: QJSValue, aTag: str = "", aParam: dict = {}) -> QObject:
        self.nextF(aFunc, aTag, aParam)
        return self

    @pyqtSlot(str)
    @pyqtSlot(str, bool)
    @pyqtSlot(str, bool, bool)
    def removeNext(self, aName: str, aAndDelete: bool = False, aOutside: bool = True):
        self.__m_parent.find(self.__m_name).removeNext(aName)
        if aAndDelete:
            self.__m_parent.remove(aName, aOutside)
    
    @pyqtSlot(str)
    @pyqtSlot(str, str)
    def removeAspect(self, aType: str, aAspect: str = ""):
        self.__m_parent.find(self.__m_name).removeAspect(aType, aAspect)

class qmlPipeline(QObject):
    def __init__(self, aName: str):
        super().__init__()
        self.__m_name = aName

    def __parseScope(self, aScope: QJSValue) ->scopeCache:
        ret = None
        if aScope.isQObject():
            sp = aScope.toQObject()
            if isinstance(sp, qmlScopeCache):
                ret = sp.m_scope
        elif aScope.isObject():
            ret = scopeCache(aScope.toVariant())
        return ret

    @pyqtSlot(str, QJSValue, result = QObject)
    @pyqtSlot(str, QJSValue, str, result = QObject)
    @pyqtSlot(str, QJSValue, str, QJSValue, result = QObject)
    def run(self, aName: str, aInput: QJSValue, aTag: str = "", aScope: QJSValue = QJSValue()) -> QObject:
        ret = qmlStream(pipelines(self.__m_name).run(aName, aInput.toVariant(), aTag, self.__parseScope(aScope)))
        qml_engine.setObjectOwnership(ret, QQmlEngine.ObjectOwnership.JavaScriptOwnership)
        return ret

    @pyqtSlot(str, QJSValue, result = QObject)
    @pyqtSlot(str, QJSValue, QJSValue, result = QObject)
    @pyqtSlot(str, QJSValue, QJSValue, bool, result = QObject)
    def call(self, aName: str, aInput: QJSValue, aScope: QJSValue = QJSValue(), aAOP: bool = True) -> QObject:
        ret = qmlStream(pipelines(self.__m_name).call(aName, aInput.toVariant(), self.__parseScope(aScope), aAOP))
        qml_engine.setObjectOwnership(ret, QQmlEngine.ObjectOwnership.JavaScriptOwnership)
        return ret

    @pyqtSlot(QJSValue, result = QObject)
    @pyqtSlot(QJSValue, str, result = QObject)
    @pyqtSlot(QJSValue, str, QJSValue, result = QObject)
    @pyqtSlot(QJSValue, str, QJSValue, bool, result = QObject)
    def input(self, aInput: QJSValue, aTag: str = "", aScope: QJSValue = QJSValue(), aAutoTag: bool = False) -> QObject:
        ret = qmlStream(pipelines(self.__m_name).input(aInput.toVariant(), aTag, self.__parseScope(aScope), aAutoTag))
        qml_engine.setObjectOwnership(ret, QQmlEngine.ObjectOwnership.JavaScriptOwnership)
        return ret

    @pyqtSlot(str)
    @pyqtSlot(str, bool)
    def remove(self, aName: str, aOutside: bool = False):
        pipelines(self.__m_name).remove(aName, aOutside)

    @pyqtSlot(QJSValue, result = QObject)
    @pyqtSlot(QJSValue, QJSValue, result = QObject)
    def add(self, aFunc: QJSValue, aParam: QJSValue = {}) -> QObject:
        if not aParam.isObject:
            return None
        ln = pipelines(self.__m_name)
        f = QJSValue(aFunc)
        def func(aStream: stream):
            f.call([qml_engine.newQObject(qmlStream(aStream))])
        ret = qmlPipe(ln, ln.add(func, aParam.toVariant()).actName())
        qml_engine.setObjectOwnership(ret, QQmlEngine.ObjectOwnership.JavaScriptOwnership)
        return ret

    @pyqtSlot(str, result = QObject)
    def find(self, aName: str) -> QObject:
        ret = qmlPipe(pipelines(self.__m_name), aName)
        qml_engine.setObjectOwnership(ret, QQmlEngine.ObjectOwnership.JavaScriptOwnership)
        return ret

class globalFuncs(QObject):
    def __init__(self):
        super().__init__()
        self.__m_pipelines = {}

    @pyqtSlot(result = QObject)
    @pyqtSlot(str, result = QObject)
    def Pipelines(self, aName: str = "py_qml") -> QObject:
        ret = self.__m_pipelines.get(aName, None)
        if ret is None:
            ret = qmlPipeline("py_qml")
            self.__m_pipelines[aName] = ret
        return ret

def createQMLPipeline(aInput: stream):
    aInput.setData(pipelineQML("qy_qml"))
pipelines().add(createQMLPipeline, {"name": "createpy_qmlpipeline"})

gf = globalFuncs()
def initRea(aInput: stream):
    global qml_engine
    qml_engine = aInput.data()
    aInput.data().rootContext().setContextObject(gf)
    aInput.out()
pipelines().add(initRea, {"name": "initRea"})