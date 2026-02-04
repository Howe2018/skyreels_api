class SkyreelsError(Exception):
    """Base exception for Skyreels SDK"""
    def __init__(self, code: int, message: str, trace_id: str = None):
        self.code = code
        self.message = message
        self.trace_id = trace_id
        super().__init__(f"[{code}] {message} (trace_id: {trace_id})")

class InvalidAPIKeyError(SkyreelsError):
    """401 Invalid API key"""
    pass

class ParameterError(SkyreelsError):
    """422 Parameter error"""
    pass

class ServiceBusyError(SkyreelsError):
    """429 Service busy"""
    pass

class InsufficientCreditsError(SkyreelsError):
    """480 Insufficient account credits"""
    pass

class QuotaExceededError(SkyreelsError):
    """481 Concurrency or QPS exceeds resource package limit"""
    pass

class InternalError(SkyreelsError):
    """500 Internal error"""
    pass

class SecurityPolicyError(SkyreelsError):
    """503 Platform security policy triggered"""
    pass

def raise_for_code(code: int, message: str, trace_id: str = None):
    if code == 200:
        return
    
    error_map = {
        401: InvalidAPIKeyError,
        422: ParameterError,
        429: ServiceBusyError,
        480: InsufficientCreditsError,
        481: QuotaExceededError,
        500: InternalError,
        503: SecurityPolicyError,
    }
    
    exc_class = error_map.get(code, SkyreelsError)
    raise exc_class(code, message, trace_id)
