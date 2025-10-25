# 1. 导入必要的库
from qiskit import QuantumCircuit
from qiskit_aer.primitives import Sampler
from qiskit.visualization import plot_histogram

# 2. 创建一个包含 3 个量子比特和 3 个经典比特的电路
qc = QuantumCircuit(3, 3)

# --- 构建 GHZ 态的核心逻辑 ---

# a. 将量子比特 0 置于叠加态
qc.h(0)

# b. 将量子比特 0 的状态“广播”给量子比特 1 和 2
qc.cx(0, 1)  # 如果 qubit 0 是 |1⟩, 则翻转 qubit 1
qc.cx(0, 2)  # 如果 qubit 0 是 |1⟩, 则翻转 qubit 2

# --------------------------------

# 3. 添加测量操作
qc.measure([0, 1, 2], [0, 1, 2])

# 4. 打印并查看我们构建的电路
print("GHZ 态量子电路：")
print(qc.draw('text'))

# 5. 使用 Sampler 运行电路
sampler = Sampler()
job = sampler.run(qc, shots=1024)
result = job.result()

# 6. 获取并打印结果
quasi_distribution = result.quasi_dists[0]
counts = quasi_distribution.binary_probabilities()

print("\n模拟结果：")
print(counts)

# 7. (可选) 绘制结果直方图
plot_histogram(counts)