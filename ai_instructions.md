# AI instructions

## Python functions

- When writing Python functions, always add docstrings in the Google style:

``` Python
def divide(a: float, b: float) -> float:
    """Divide two numbers.

    Args:
        a: The dividend.
        b: The divisor.

    Returns:
        The quotient of a divided by b.

    Raises:
        ZeroDivisionError: If b is zero.
    """
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b
```

## Keep it simple

Write code that my future self will understand right away.
This is a great example:

``` Python 
def process_order(order_details):
  order_is_valid = validate_order(order_details)
  if not order_is_valid:
    return "Error: order is not valid"
  payment_is_valid = process_payment(order_details)
  if payment_is_valid:
    save_order(order_details)
    return "OK: order processed successfully"
  else:
    return "Error: payment is not valid"
```

## System prompt

- Suggest only code that a junior developer would understand.
- Don't create unnecessary comments.
  For instance don't write `# load data` when the next line is `load_file(filename)`
