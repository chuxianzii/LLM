from colorama import Fore, Style, init


def log_title(message: str) -> None:
    init()  # 初始化colorama
    total_length = 80
    message_length = len(message)
    padding = max(0, total_length - message_length - 4)  # 4 for the "=="
    left_padding = padding // 2
    right_padding = padding - left_padding  # 确保两边对称

    padded_message = f"{'=' * left_padding} {message} {'=' * right_padding}"

    # 使用colorama设置颜色效果
    colored_message = f"{Style.BRIGHT}{Fore.CYAN}{padded_message}{Style.RESET_ALL}"
    print(colored_message)


# 使用示例
log_title("Hello World")
