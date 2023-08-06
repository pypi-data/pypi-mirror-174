import os
__APPLICATION_PATH__ = os.path.dirname(__file__)
__APPLICATION_DATA__ = __APPLICATION_PATH__ + "/Data"

if not os.path.exists(__APPLICATION_DATA__):
	os.makedirs(__APPLICATION_DATA__)

print("application data file path", __APPLICATION_DATA__)



__APPLICATION_DATABASE_PATH__ = __APPLICATION_DATA__ + "/sim.db"

__DEFAULT_CONTROLLER_SOCKET__ = 'http://srv01.letscode.it:9851/'