import subprocess
import time

print("🚀 Запускаем сервер...")
server_process = subprocess.Popen(["poetry", "run", "python", "run_server.py"])

# Ждём запуска сервера
time.sleep(3)

print("🧪 Запускаем нагрузочное тестирование...")
result = subprocess.run(
    [
        "poetry",
        "run",
        "locust",
        "-f",
        "tests/load/test_load.py",
        "--headless",
        "--users",
        "50",
        "--spawn-rate",
        "10",
        "--run-time",
        "30s",
        "--csv",
        "loadtest_results",
    ]
)

print("✅ Нагрузочное тестирование завершено.")

# Останавливаем сервер
server_process.terminate()
server_process.wait()

print("📊 Результаты тестирования:")
with open("loadtest_results_stats.csv", "r") as f:
    print(f.read())
