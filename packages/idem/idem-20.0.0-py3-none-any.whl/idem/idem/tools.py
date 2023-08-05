import copy
import fnmatch
import inspect
from typing import Any
from typing import Dict
from typing import List


def gen_tag(hub, chunk):
    """
    Generate the unique tag used to track the execution of the chunk
    """
    return f'{chunk["state"]}_|-{chunk["__id__"]}_|-{chunk["name"]}_|-{chunk["fun"]}'


def get_chunks(hub, low, state, name):
    """
    Search in the low state for the chunk with the given designation
    """
    rets = []
    for chunk in low:
        if state == "sls":
            if fnmatch.fnmatch(chunk["__sls__"], name):
                rets.append(chunk)
                continue
        if state == chunk["state"]:
            if fnmatch.fnmatch(chunk["name"], name) or fnmatch.fnmatch(
                chunk["__id__"], name
            ):
                rets.append(chunk)
    return rets


def find_name(hub, name, state, high):
    """
    Scan high data for the id referencing the given name and return a list of (IDs, state) tuples that match
    Note: if `state` is sls, then we are looking for all IDs that match the given SLS
    """
    ext_id = []
    if name in high:
        ext_id.append((name, state))
    # if we are requiring an entire SLS, then we need to add ourselves to everything in that SLS
    elif state == "sls":
        for nid, item in high.items():
            if item["__sls__"] == name:
                ext_id.append((nid, next(iter(item))))
    # otherwise we are requiring a single state, lets find it
    else:
        # We need to scan for the name
        for nid in high:
            if state in high[nid]:
                if isinstance(high[nid][state], list):
                    for arg in high[nid][state]:
                        if not isinstance(arg, dict):
                            continue
                        if len(arg) != 1:
                            continue
                        if arg[next(iter(arg))] == name:
                            ext_id.append((nid, state))
    return ext_id


def format_call(
    hub,
    fun,
    data,
    ignore_changes: List = None,
    initial_ret=None,
    expected_extra_kws=(),
    is_class_method=None,
    enforced_state: Dict[str, Any] = None,
):
    """
    Build the required arguments and keyword arguments required for the passed
    function.
    :param fun: The function to get the argspec from
    :param data: A dictionary containing the required data to build the
                 arguments and keyword arguments.
    :param ignore_changes: A list of path of parameters that will be assigned to None value
                           to ignore being updated in present().
    :param initial_ret: The initial return data pre-populated as dictionary or
                        None
    :param expected_extra_kws: Any expected extra keyword argument names which
                               should not trigger a :ref:`SaltInvocationError`
    :param is_class_method: Pass True if you are sure that the function being passed
                            is a class method. The reason for this is that on Python 3
                            ``inspect.ismethod`` only returns ``True`` for bound methods,
                            while on Python 2, it returns ``True`` for bound and unbound
                            methods. So, on Python 3, in case of a class method, you'd
                            need the class to which the function belongs to be instantiated
                            and this is not always wanted.
    :param enforced_state: A dictionary with the parameters from a previous run
    :returns: A dictionary with the function required arguments and keyword
              arguments.
    """
    ret = initial_ret is not None and initial_ret or {}
    enforced_state = enforced_state or {}

    ret["args"] = []
    ret["kwargs"] = {}
    args = []
    kwargs = {}
    keywords = False

    sig = fun.signature
    for name, param in sig.parameters.items():
        if name == "hub":
            continue
        elif param.kind.name == "POSITIONAL_OR_KEYWORD":
            if param.default is inspect._empty:
                if name in enforced_state:
                    # get it from enforced state before default
                    kwargs[name] = enforced_state[name]
                else:
                    args.append(name)
            else:
                kwargs[name] = enforced_state.get(name, param.default)
                # Validate a boolean value for arguments of type boolean
                if isinstance(param.default, bool):
                    if data.get(name) and not isinstance(data.get(name), bool):
                        raise TypeError(
                            f"{fun.ref}.{fun.func.__name__} is expecting a boolean value for '{name}' but got '{data.get(name)}'"
                        )
        elif param.kind.name == "KEYWORD_ONLY":
            # get it from enforced state before default
            kwargs[name] = enforced_state.get(name, param.default)
        elif param.kind.name == "VAR_KEYWORD":
            keywords = True
    ret["avail_kwargs"] = copy.copy(kwargs)
    ret["avail_args"] = copy.copy(args)
    ret["keywords"] = keywords

    # Since we WILL be changing the data dictionary, let's change a copy of it
    data = data.copy()
    is_existing_resource = bool(enforced_state) or bool(data.get("resource_id"))

    missing_args = []

    for key in kwargs:
        try:
            # Do not override enforced_state value with None,
            # unless no value is set
            val = data.pop(key)
            if val is not None or kwargs[key] is inspect._empty:
                kwargs[key] = val

            # if the execution flow is for recreating a resource,
            # then we should override enforced_state value with None for resource_id
            if key == "resource_id" and data.get("recreation_flow", False):
                kwargs[key] = val
        except KeyError:
            # Let's leave the default value in place
            pass

    # If ignore_changes contains parameters, then we try to assign those parameters with None to skip updating.
    # For resource recreation flow, we should not nullify the parameters in ignore_changes.
    if (
        ignore_changes
        and is_existing_resource
        and not data.get("recreation_flow", False)
    ):
        hub.idem.tool.ignore_changes.ignore_parameter_changes(
            ignore_changes=ignore_changes,
            params=kwargs,
            param_signatures=sig.parameters,
        )

    while args:
        arg = args.pop(0)
        try:
            ret["args"].append(data.pop(arg))
        except KeyError:
            missing_args.append(arg)

    if missing_args:
        raise ValueError(
            f"{fun.ref}.{fun.func.__name__} is missing required argument(s): {', '.join(missing_args)}"
        )

    ret["kwargs"].update(kwargs)

    if keywords:
        # The function accepts **kwargs, any non expected extra keyword
        # arguments will made available.
        for key, value in data.items():
            if key in expected_extra_kws:
                continue
            ret["kwargs"][key] = value

        # No need to check for extra keyword arguments since they are all
        # **kwargs now. Return
        return ret

    # Did not return yet? Lets gather any remaining and unexpected keyword
    # arguments
    extra = {}
    for key, value in data.items():
        if key in expected_extra_kws:
            continue
        extra[key] = copy.deepcopy(value)

    if extra:
        # Found unexpected keyword arguments, raise an error to the user
        if len(extra) == 1:
            msg = "'{0[0]}' is an invalid keyword argument for '{1}'".format(
                list(extra.keys()),
                ret.get(
                    # In case this is being called for a state module
                    "full",
                    # Not a state module, build the name
                    f"{fun.__module__}.{fun.__name__}",
                ),
            )
        else:
            msg = "{} and '{}' are invalid keyword arguments for '{}'".format(
                ", ".join([f"'{e}'" for e in extra][:-1]),
                list(extra.keys())[-1],
                ret.get(
                    # In case this is being called for a state module
                    "full",
                    # Not a state module, build the name
                    f"{fun.__module__}.{fun.__name__}",
                ),
            )
    return ret


def ishashable(hub, obj):
    """
    A simple test to verify if a given object is hashable and can therefore
    be used as a key in a dict
    """
    try:
        hash(obj)
    except TypeError:
        return False
    return True


def iter_high(hub, high):
    """
    Take a high-state structure and iterate over it yielding the elements down to the
    execution args
    Yields (id_, body, state, run, arg)
    """
    for id_, body in high.items():
        if not isinstance(body, dict):
            continue
        for state, run in body.items():
            if state.startswith("__"):
                continue
            for arg in run:
                yield id_, body, state, run, arg


def iter_high_leaf_args(hub, high):
    """
    Take a high-state structure and iterate over it yielding the elements down to the
    execution args
    Yields (id_, body, state, run, arg)
    """
    for id_, body in high.items():
        if not isinstance(body, dict):
            continue
        for state, run in body.items():
            if state.startswith("__"):
                continue
            for arg in run:
                yield from _iter_arg_chain(id_, body, state, run, "", arg)


def _iter_arg_chain(id_, body, state, run, arg_key_def, arg):
    if isinstance(arg, dict):
        for arg_key, arg_value in arg.items():
            # Escape dictionary references in the key definition to skip evaluating by arg_bind resolver.
            arg_key = arg_key.replace("[", "[\\")
            if arg_key_def:
                current_arg_key_def = arg_key_def + ":" + arg_key
            else:
                current_arg_key_def = arg_key

            if isinstance(arg_value, dict):
                yield from _iter_arg_chain(
                    id_, body, state, run, current_arg_key_def, arg_value
                )
            elif isinstance(arg_value, list):
                for index, arg_value_item in enumerate(arg_value):
                    yield from _iter_arg_chain(
                        id_,
                        body,
                        state,
                        run,
                        current_arg_key_def + f"[{index}]",
                        arg_value_item,
                    )
            else:
                yield id_, body, state, run, current_arg_key_def, arg_value
    elif isinstance(arg, list):
        for index, arg_value_item in enumerate(arg):
            yield from _iter_arg_chain(
                id_, body, state, run, arg_key_def + f"[{index}]", arg_value_item
            )
    else:
        yield id_, body, state, run, arg_key_def, arg


def get_enforced_state(hub, chunk, managed_state):
    tag = hub.idem.tools.gen_tag(chunk)
    esm_tag = hub.idem.managed.gen_tag(chunk)
    new_chunk = {**chunk, "__id__": f"{chunk['__id__']}_create_new"}
    new_tag = hub.idem.tools.gen_tag(new_chunk)
    new_esm_tag = hub.idem.managed.gen_tag(new_chunk)

    enforced_state = managed_state.get(new_esm_tag) or managed_state.get(new_tag)

    if not enforced_state:
        enforced_state = managed_state.get(esm_tag) or managed_state.get(tag)

    return enforced_state
