from graphviz import Digraph

def create_dfd_diagram():
    dfd = Digraph(format="png", filename="logical_dfd_diagram")

    # Adding entities
    dfd.node("Customer", "Customer", shape="rectangle", style="filled", color="#A8D5BA")
    dfd.node("Prices", "Prices", shape="parallelogram", style="filled", color="#A8D5BA")

    # Adding processes
    dfd.node("P1", "Identify Item", shape="box", style="filled", color="#9BD1A5")
    dfd.node("P2", "Look up Prices", shape="box", style="filled", color="#9BD1A5")
    dfd.node("P3", "Compute Total Cost of Order", shape="box", style="filled", color="#9BD1A5")
    dfd.node("P4", "Settle Transaction\nand Issue Receipt", shape="box", style="filled", color="#9BD1A5")

    # Adding data flows
    dfd.edge("Customer", "P1", label="items to purchase")
    dfd.edge("P1", "Prices", label="item ID")
    dfd.edge("Prices", "P2", label="prices")
    dfd.edge("P1", "P2", label="items")
    dfd.edge("P2", "P3", label="items and prices")
    dfd.edge("P3", "P4", label="amount to be paid")
    dfd.edge("Customer", "P4", label="payment")
    dfd.edge("P4", "Customer", label="receipt")

    # Rendering diagram
    dfd.render(view=True)

create_dfd_diagram()