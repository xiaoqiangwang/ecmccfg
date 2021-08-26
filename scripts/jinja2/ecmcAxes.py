from ecmcYamlHandler import *
from ecmcJinja2 import JinjaTemplate


class EcmcAxis(YamlHandler):
    def __init__(self, axisconfig, jinjatemplatedir):
        super().__init__()
        self.jinjatemplatedir = jinjatemplatedir
        self.loadYamlData(axisconfig)
        self.setEcmcAxisType()
        self.config = None

    def create(self):
        if self.axisType == 1:
            self.config = EcmcJoint(self.yamlData, self.jinjatemplatedir)
        else:
            self.config = EcmcEndEffector(self.yamlData, self.jinjatemplatedir)


class EcmcCommonAxis(JinjaTemplate):
    def __init__(self, _jinjatemplatedir, _configuration):
        super(EcmcCommonAxis, self).__init__(directory=_jinjatemplatedir, templateFile=None)
        self.configuration = _configuration
        self.axisType = self.configuration['axis']['EcmcType']
        self.setAxisTemplate()

    def setAxisTemplate(self):
        axisTemplate = {
            1: 'joint.jinja2',
            2: 'endEffector.jinja2',
        }
        self.read(axisTemplate[self.axisType])


class EcmcEndEffector(EcmcCommonAxis):
    def __init__(self, _configuration, _jinjatemplatedir):
        super(EcmcEndEffector, self).__init__(_jinjatemplatedir=_jinjatemplatedir, _configuration=_configuration)
        self.pruneConfiguration()

    def pruneConfiguration(self):
        self.configuration['drive'] = None
        self.configuration['controller'] = None


class EcmcJoint(EcmcCommonAxis):
    def __init__(self, _configuration, _jinjatemplatedir):
        super(EcmcJoint, self).__init__(_jinjatemplatedir=_jinjatemplatedir, _configuration=_configuration)


if __name__ == '__main__':
    # axis = EcmcAxis('./test/testEndEffector.yaml', './templates/')
    axis = EcmcAxis('./test/testJoint.yaml', './templates/')
    axis.create()
    axis.config.render(axis.yamlData)
    axis.config.show()

