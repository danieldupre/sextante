class Output(object):

#===============================================================================
#    @property
#    def value(self):
#        return self._value
#
#    @value.setter
#    def value(self, value):
#        self._value = value
#
#    @property
#    def name(self):
#        return self._name
#
#    @name.setter
#    def name(self, name):
#        self._name = name
#
#    @property
#    def description(self):
#        return self._description
#
#    @description.setter
#    def description(self, description):
#        self._description = description
#
#    @property
#    def channel(self):
#        return self._channel
#
#    @channel.setter
#    def channel(self, channel):
#        self._channel = channel
#===============================================================================


    def __str__(self):
        return self.name + " <" + self.__module__.split(".")[-1] +">"

