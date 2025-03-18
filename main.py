import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import matplotlib.animation as animation

# Загружаем данные
data_rk4 = np.loadtxt("duffing_rk4.dat")
data_dp = np.loadtxt("duffing_dp.dat")
data_diff = np.loadtxt("diff.dat")  # Теперь содержит avg_local_diff_x и avg_local_diff_v

N = data_rk4.shape[1] // 2  # Число точек
steps = data_rk4.shape[0]   # Количество временных шагов

x_rk4 = data_rk4[:, 0::2]
v_rk4 = data_rk4[:, 1::2]
x_dp = data_dp[:, 0::2]
v_dp = data_dp[:, 1::2]
avg_diff_x = data_diff[:, 0]  # Средняя локальная ошибка по x
avg_diff_v = data_diff[:, 1]  # Средняя локальная ошибка по v

time = np.linspace(0, 200.0, steps)

# Создаем фигуру
fig = plt.figure(figsize=(18, 12))
plt.subplots_adjust(bottom=0.2)

# Графики фазового пространства
ax1 = plt.subplot(2, 2, 1)
ax2 = plt.subplot(2, 2, 2)
# Графики разностей
ax4 = plt.subplot(2, 2, 3)
ax5 = plt.subplot(2, 2, 4)

# Настройка фазовых графиков
for ax in (ax1, ax2):
    ax.set_xlim(np.min([x_rk4, x_dp]) - 0.5, np.max([x_rk4, x_dp]) + 0.5)
    ax.set_ylim(np.min([v_rk4, v_dp]) - 0.5, np.max([v_rk4, v_dp]) + 0.5)
    ax.set_xlabel("x")
    ax.set_ylabel("v")

ax1.set_title("RK4")
ax2.set_title("Dormand-Prince 8(5,3)")

# Настройка графиков ошибок
ax4.set_xlabel("Time")
ax4.set_ylabel("Average |x_RK4 - x_DP8|")
ax4.set_title("Average Local Error in x")
ax4.set_xlim(0, 200.0)
ax4.set_ylim(0, 3.5)  # Устанавливаем максимальное значение для оси Y

ax5.set_xlabel("Time")
ax5.set_ylabel("Average |v_RK4 - v_DP8|")
ax5.set_title("Average Local Error in v")
ax5.set_xlim(0, 200.0)
ax5.set_ylim(0, 3.5)  # Устанавливаем максимальное значение для оси Y

# Графические объекты
points_rk4 = ax1.scatter(x_rk4[0], v_rk4[0], c=np.linspace(0, 1, N), cmap='plasma', s=10)
points_dp = ax2.scatter(x_dp[0], v_dp[0], c=np.linspace(0, 1, N), cmap='plasma', s=10)
line_x, = ax4.plot([], [], 'b-', label='Error in x')
line_v, = ax5.plot([], [], 'r-', label='Error in v')

ax4.legend()
ax5.legend()

# Добавляем виджеты
ax_slider = plt.axes([0.15, 0.05, 0.7, 0.03])
ax_play = plt.axes([0.15, 0.01, 0.1, 0.03])
ax_stop = plt.axes([0.3, 0.01, 0.1, 0.03])

slider = Slider(ax_slider, 'Time', 0, steps - 1, valinit=0, valstep=1)
button_play = Button(ax_play, 'Play')
button_stop = Button(ax_stop, 'Stop')

anim = None
current_frame = 0

# Функция обновления графиков
def update(frame):
    points_rk4.set_offsets(np.column_stack((x_rk4[frame], v_rk4[frame])))
    points_dp.set_offsets(np.column_stack((x_dp[frame], v_dp[frame])))
    line_x.set_data(time[:frame + 1], avg_diff_x[:frame + 1])
    line_v.set_data(time[:frame + 1], avg_diff_v[:frame + 1])
    points_rk4.set_visible(True)
    points_dp.set_visible(True)
    line_x.set_visible(True)
    line_v.set_visible(True)
    fig.canvas.draw_idle()

# Функция для слайдера
def update_slider(val):
    global current_frame
    current_frame = int(val)
    update(current_frame)

# Функция анимации
def animate(frame):
    global current_frame
    current_frame = frame
    points_rk4.set_offsets(np.column_stack((x_rk4[frame], v_rk4[frame])))
    points_dp.set_offsets(np.column_stack((x_dp[frame], v_dp[frame])))
    line_x.set_data(time[:frame + 1], avg_diff_x[:frame + 1])
    line_v.set_data(time[:frame + 1], avg_diff_v[:frame + 1])
    slider.set_val(frame)
    return points_rk4, points_dp, line_x, line_v

# Функция запуска анимации
def play(event):
    global anim
    if anim is None or anim.event_source is None:
        anim = animation.FuncAnimation(
            fig, animate, frames=range(current_frame, steps), interval=5, blit=False, repeat=True
        )
    fig.canvas.draw_idle()

# Функция остановки анимации
def stop(event):
    global anim
    if anim is not None:
        anim.event_source.stop()
        anim = None
    update(current_frame)

slider.on_changed(update_slider)
button_play.on_clicked(play)
button_stop.on_clicked(stop)

update(0)

plt.show()