from typing import Any, get_origin, get_args
from types import UnionType

def is_instance_of_type(obj: Any, expected_type: Any) -> bool:
    """
    Check if an object matches a given type, supporting complex type hints.
    
    :param obj: The object to check
    :param expected_type: The type or type hint to match against
    
    :return: True if the object matches the type, False otherwise.
    """
    # Handle None
    if expected_type is type(None) or expected_type is None:
        return obj is None
    
    base_type = get_origin(expected_type)
    type_args = get_args(expected_type)

    # Standard isinstance check for non-parametric types
    if base_type is None:
        return isinstance(obj, expected_type)
    
    # Handle Unions
    if base_type is UnionType:
        return any(is_instance_of_type(obj, t) for t in type_args)
    
    # Handle parametric types (like List[str], Tuple[int, ...])
    if not isinstance(obj, base_type):
        return False
    
    # For variable-length containers (ellipsis (...) or single type argument)
    if type_args[-1] is ... or len(type_args) == 1:
        return all(is_instance_of_type(item, type_args[0]) for item in obj)
    # For fixed-length containers, check each item against corresponding type
    else:
        return (
            len(type_args) == len(obj)
            and all(
                is_instance_of_type(item, arg_type) 
                for item, arg_type in zip(obj, type_args)
            )
        )
    
    
