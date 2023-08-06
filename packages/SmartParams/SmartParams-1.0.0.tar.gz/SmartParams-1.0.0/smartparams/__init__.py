from smartparams.register import SmartObject, SmartRegister
from smartparams.smart import Smart
from smartparams.utils.loggers import Log

__all__ = [
    'Smart',
    'SmartRegister',
    'SmartObject',
]

# TYPES --------------------------------------------------------------------------------------------
import smartparams.types.builtins.bool as _bool
import smartparams.types.builtins.dict as _dict
import smartparams.types.builtins.float as _float
import smartparams.types.builtins.int as _int
import smartparams.types.builtins.list as _list
import smartparams.types.builtins.none as _none
import smartparams.types.builtins.set as _set
import smartparams.types.builtins.str as _str
import smartparams.types.builtins.tuple as _tuple
import smartparams.types.pathlib.path as _path
import smartparams.types.smartparams.smart as _smart
import smartparams.types.typing.any as _any
import smartparams.types.typing.callable as _callable
import smartparams.types.typing.forwardref as _forwardref
import smartparams.types.typing.type as _type

# RESOLVERS ----------------------------------------------------------------------------------------
from smartparams.resolvers.missing import missing_value_resolver

# BUILTINS -----------------------------------------------------------------------------------------
_bool.register()
_dict.register()
_float.register()
_int.register()
_list.register()
_none.register()
_set.register()
_str.register()
_tuple.register()

# PATHLIB ------------------------------------------------------------------------------------------
_path.register()

# SMARTPARAMS --------------------------------------------------------------------------------------
_smart.register()

# TYPING -------------------------------------------------------------------------------------------
_any.register()
_callable.register()
_forwardref.register()
_type.register()

# RESOLVERS ----------------------------------------------------------------------------------------
Smart.register.resolvers.append(missing_value_resolver)

# LOGGING ------------------------------------------------------------------------------------------
Log.setup()
