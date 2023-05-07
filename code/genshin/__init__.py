'''
# user
import user.login as login
import user.register as register
import user.changeUserInfo as changeUserInfo

# equipment
import equipment.connectEquipment as connectEquipment
import equipment.disconnectEquipment as disconnectEquipment

# data
import data.getData as getData
import data.discardData as discardData
import data.changeLabel as changeLabel
import data.collectData as collectData
import data.collectDataStop as collectDataStop
import data.getPrediction as getPrediction
'''
from .user import *
from .equipment import *
from .data import *