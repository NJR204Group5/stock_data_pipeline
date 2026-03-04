import sys
import argparse
from tasks.get_twse_listed_stocks import run as run_stock_list
from tasks.fetch_all_stocks_history import run as run_stock_history

TASKS = {
    "stock_list": run_stock_list,
    "stock_history": run_stock_history,
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "task",
        nargs="?",
        default="stock_list",
        choices=TASKS.keys(),
        help="選擇要執行的任務"
    )
    args = parser.parse_args()

    try:
        TASKS[args.task]()
        print("任務執行完成")
    except Exception as e:
        print(f"任務執行失敗: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

# fetch_full_history('1101', "台泥", 1910, 1, True)