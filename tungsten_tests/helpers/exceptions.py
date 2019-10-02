class TFTException(Exception):
    """Base class for exceptions in TungstenFabric Tests."""
    message = "An unknown exception occurred"

    def __init__(self, *args, **kwargs):
        super(TFTException, self).__init__()
        try:
            self._error_string = self.message.format(**kwargs)
        except Exception:
            # at least get the core message out if something happened
            self._error_string = self.message
        if args:
            # If there is a non-kwarg parameter, assume it's the error
            # message or reason description and tack it on to the end
            # of the exception message
            # Convert all arguments into their string representations...
            # args = ["{}".format(arg for arg in args)]
            # self._error_string = (self._error_string +
            #                       "\nDetails:\n%s" % '\n'.join(args))
            self._error_string = (self._error_string + "\nDetails:\n")
            for arg in args:
                self._error_string = self._error_string + '{}\n'.format(arg)

    def __str__(self):
        return self._error_string


class TFTConfigPathIsNotSet(TFTException):
    message = "TFT_CONFIG path isn't set !"


class TFTKubeConfigPathIsNotSet(TFTException):
    message = "TFT_KUBECONFIG path isn't set !"


class FileNotFoundError(TFTException):
    message = "File {path} doesnt exist."


class TimeoutException(TFTException):
    message = "Request timed out."


class InterfaceNotFoundException(TFTException):
    message = "Instance {instance_id} hasn't interface from network {net_id}."


class InstanceNotReady(TFTException):
    message = "Cloud instance initialization wasn't done in time."


class OpenStackClientException(TFTException):
    pass


class BuildErrorException(OpenStackClientException):
    message = "Instance {instance_id} failed to build and is in ERROR status."
