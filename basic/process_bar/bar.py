import sys
import time

def progress_bar(iterable, prefix='', length=30, fill='█', print_end='\r'):
  total = len(iterable)
  progress = 0

  def print_bar(progress):
    percent = ("{0:.1f}").format(100 * (progress / float(total)))
    filled_length = int(length * progress // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% Complete')
    sys.stdout.flush()

  for item in iterable:
    yield item
    progress += 1
    print_bar(progress)

  sys.stdout.write(print_end)
  sys.stdout.flush()
  print_bar(progress)

# 示例用法
items = list(range(0, 100))
print("introduct someting...")
for _ in progress_bar(items, prefix='Progress:', length=100):
  # 模拟耗时操作
  time.sleep(0.1)
