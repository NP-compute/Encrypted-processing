from src.logic_gate import perform_not_example, perform_nand_example

def test_perform_not_example():
    assert perform_not_example(0) == 1
    assert perform_not_example(1) == 0

def test_perform_nand_example():
    assert perform_nand_example(0, 0) == 1
    assert perform_nand_example(0, 1) == 1
    assert perform_nand_example(1, 0) == 1
    assert perform_nand_example(1, 1) == 0

if __name__ == "__main__":
    test_perform_not_example()
    test_perform_nand_example()
    print("All tests passed.")