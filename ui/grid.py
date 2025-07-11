def print_grid(items, cols=2, width=40):
    # Simple grid for CLI, Termux friendly
    for i, item in enumerate(items):
        print(f"{item:<{width}}", end="" if (i+1) % cols else "\n")
    if len(items) % cols:
        print()