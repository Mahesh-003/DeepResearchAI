import ast
import operator

from retriever import retrieve_relevant_research


# ==========================================
# CALCULATOR TOOL
# ==========================================

def calculator(expression):

    try:
        allowed_operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.Mod: operator.mod,
        }

        def calculate(node):

            if isinstance(node, ast.Constant):
                if isinstance(node.value, (int, float)):
                    return node.value

            if isinstance(node, ast.BinOp):

                left = calculate(node.left)
                right = calculate(node.right)

                operation = allowed_operators.get(
                    type(node.op)
                )

                if operation is None:
                    raise ValueError(
                        "Operator not allowed"
                    )

                return operation(left, right)

            if isinstance(node, ast.UnaryOp):

                value = calculate(node.operand)

                if isinstance(node.op, ast.USub):
                    return -value

                if isinstance(node.op, ast.UAdd):
                    return value

            raise ValueError(
                "Invalid mathematical expression"
            )

        tree = ast.parse(
            expression,
            mode="eval"
        )

        return calculate(tree.body)

    except Exception as e:

        return f"Calculator error: {e}"


# ==========================================
# KNOWLEDGE SEARCH TOOL
# ==========================================

def search_knowledge(query):

    results = retrieve_relevant_research(query)

    if not results:
        return "No relevant research found."

    output = []

    for result in results:

        output.append(
            f"""
Title:
{result.get("title", "")}

Question:
{result.get("question", "")}

Research:
{result.get("result", "")}
"""
        )

    return "\n".join(output)


# ==========================================
# TEST TOOLS
# ==========================================

if __name__ == "__main__":

    print("🛠️ TOOL TEST")
    print("=" * 50)

    print("\nCalculator:")
    print(
        calculator("25 * 4 + 10")
    )

    print("\nKnowledge Search:")
    print(
        search_knowledge(
            "Generative AI developer productivity"
        )
    )
    