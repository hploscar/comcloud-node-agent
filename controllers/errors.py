class ControllerError(Exception):
    pass

class ResourceExistsError(ControllerError):
    pass

class PlatformNotSupportedError(ControllerError):
    pass

class InstallationError(ControllerError):
    pass
