from mcp.server import MCPServer

mcp = MCPServer("Banking Tools")


@mcp.tool()
def get_account_balance(account_number: str) -> dict:
    """
    Get the current balance of a bank account.
    """

    accounts = {
        "12345": 15000,
        "67890": 25000,
        "11111": 5000
    }

    balance = accounts.get(account_number)

    if balance is None:
        return {
            "error": "Account not found"
        }

    return {
        "account_number": account_number,
        "balance": balance,
        "currency": "INR"
    }


@mcp.tool()
def get_customer_name(account_number: str) -> str:
    """
    Get customer name using account number.
    """

    customers = {
        "12345": "Rahul",
        "67890": "Amit",
        "11111": "Priya"
    }

    return customers.get(account_number, "Unknown")


if __name__ == "__main__":
    mcp.run()