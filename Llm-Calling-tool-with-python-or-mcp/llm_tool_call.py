import sys
import io

sys.stdout = io.TextIOWrapper(
    sys.stdout.buffer,
    encoding="utf-8"
)

sys.stderr = io.TextIOWrapper(
    sys.stderr.buffer,
    encoding="utf-8"
)

from ollama import chat

# ============================================================
# 1. Python tools
# ============================================================

def get_account_balance(account_number: str):
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


def get_customer_name(account_number: str):
    customers = {
        "12345": "Rahul",
        "67890": "Amit",
        "11111": "Priya"
    }

    return {
        "account_number": account_number,
        "customer_name": customers.get(account_number, "Unknown")
    }


# ============================================================
# 2. Describe tools to the LLM
# ============================================================

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_account_balance",
            "description": "Get the current balance of a bank account",
            "parameters": {
                "type": "object",
                "properties": {
                    "account_number": {
                        "type": "string",
                        "description": "Bank account number"
                    }
                },
                "required": ["account_number"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_customer_name",
            "description": "Get customer name using account number",
            "parameters": {
                "type": "object",
                "properties": {
                    "account_number": {
                        "type": "string",
                        "description": "Bank account number"
                    }
                },
                "required": ["account_number"]
            }
        }
    }
]


# ============================================================
# 3. User message
# ============================================================

messages = [
    {
        "role": "user",
        "content": "What is the balance of account 12345?"
    }
]


# ============================================================
# 4. First LLM call
# ============================================================

response = chat(
    model="llama3.2:latest",
    messages=messages,
    tools=tools
)


print("\nInitial LLM response:")
print(response)


# ============================================================
# 5. Check if LLM wants to call a tool
# ============================================================

if response.message.tool_calls:

    # IMPORTANT:
    # Convert Ollama Message object into a dictionary
    # before adding it to messages.
    
    messages.append(
        response.message.model_dump(exclude_none=True)
    )


    # ========================================================
    # 6. Execute requested tools
    # ========================================================

    for tool_call in response.message.tool_calls:

        tool_name = tool_call.function.name
        arguments = tool_call.function.arguments

        print("\n==============================")
        print("Tool requested:", tool_name)
        print("Arguments:", arguments)
        print("==============================")


        # ----------------------------------------------------
        # Execute Python function
        # ----------------------------------------------------

        if tool_name == "get_account_balance":

            result = get_account_balance(
                arguments["account_number"]
            )

        elif tool_name == "get_customer_name":

            result = get_customer_name(
                arguments["account_number"]
            )

        else:

            result = {
                "error": f"Unknown tool: {tool_name}"
            }


        print("\nTool result:")
        print(result)


        # ====================================================
        # 7. Send tool result back to LLM
        # ====================================================

        messages.append(
            {
                "role": "tool",
                "content": str(result)
            }
        )


    # ========================================================
    # 8. Ask LLM to generate final response
    # ========================================================

    final_response = chat(
        model="llama3.2:latest",
        messages=messages,
        tools=tools
    )


    print("\n=================================")
    print("FINAL LLM RESPONSE")
    print("=================================")

    print(final_response.message.content)


else:

    print("\nLLM answered directly:")
    print(response.message.content)