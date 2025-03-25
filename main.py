import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import matplotlib.animation as animation

# Загружаем данные
data_rk4 = np.loadtxt("duffing_rk4.dat")
data_dp8 = np.loadtxt("duffing_dp8.dat")
data_rk6 = np.loadtxt("duffing_rk6.dat")
data_diff_rk4_dp8 = np.loadtxt("diff_rk4_dp8.dat")  # Локальные разности RK4 vs Dopri8
data_diff_rk6_dp8 = np.loadtxt("diff_rk6_dp8.dat")  # Локальные разности RK6 vs Dopri8

N = data_rk4.shape[1] // 2  # Число частиц (количество пар x, v)
steps = data_rk4.shape[0]   # Количество временных шагов

# Извлекаем координаты и скорости
x_rk4 = data_rk4[:, 0::2]  # Координаты x для RK4
v_rk4 = data_rk4[:, 1::2]  # Скорости v для RK4
x_dp8 = data_dp8[:, 0::2]  # Координаты x для Dopri8
v_dp8 = data_dp8[:, 1::2]  # Скорости v для Dopri8
x_rk6 = data_rk6[:, 0::2]  # Координаты x для RK6
v_rk6 = data_rk6[:, 1::2]  # Скорости v для RK6

# Извлекаем средние локальные разности
avg_diff_x_rk4_dp8 = data_diff_rk4_dp8[:, 0]  # Средняя локальная ошибка по x (RK4 vs Dopri8)
avg_diff_v_rk4_dp8 = data_diff_rk4_dp8[:, 1]  # Средняя локальная ошибка по v (RK4 vs Dopri8)
avg_diff_x_rk6_dp8 = data_diff_rk6_dp8[:, 0]  # Средняя локальная ошибка по x (RK6 vs Dopri8)
avg_diff_v_rk6_dp8 = data_diff_rk6_dp8[:, 1]  # Средняя локальная ошибка по v (RK6 vs Dopri8)

time = np.linspace(0, 200.0, steps)  # Временная шкала

# Создаем фигуру
fig = plt.figure(figsize=(18, 12))
plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.2, hspace=0.3)

# Графики фазового пространства
ax1 = plt.subplot(2, 3, 1)  # RK4
ax2 = plt.subplot(2, 3, 2)  # Dopri8
ax3 = plt.subplot(2, 3, 3)  # RK6
# Графики разностей
ax4 = plt.subplot(2, 3, 4)  # Ошибки RK4 vs Dopri8
ax5 = plt.subplot(2, 3, 5)  # Ошибки RK6 vs Dopri8

# Настройка фазовых графиков
for ax in (ax1, ax2, ax3):
    ax.set_xlim(np.min([x_rk4, x_dp8, x_rk6]) - 0.5, np.max([x_rk4, x_dp8, x_rk6]) + 0.5)
    ax.set_ylim(np.min([v_rk4, v_dp8, v_rk6]) - 0.5, np.max([v_rk4, v_dp8, v_rk6]) + 0.5)
    ax.set_xlabel("x")
    ax.set_ylabel("v")

ax1.set_title("RK4")
ax2.set_title("Dopri8")
ax3.set_title("RK6")

# Настройка графиков ошибок
ax4.set_xlabel("Time")
ax4.set_ylabel("Average |x - x_Dopri8|")
ax4.set_title("Average Local Error in x (RK4 vs Dopri8)")
ax4.set_xlim(0, 200.0)
ax4.set_ylim(0, np.max([avg_diff_x_rk4_dp8, avg_diff_v_rk4_dp8]) * 1.1)  # Динамическая шкала

ax5.set_xlabel("Time")
ax5.set_ylabel("Average |x - x_Dopri8|")
ax5.set_title("Average Local Error in x (RK6 vs Dopri8)")
ax5.set_xlim(0, 200.0)
ax5.set_ylim(0, np.max([avg_diff_x_rk6_dp8, avg_diff_v_rk6_dp8]) * 1.1)  # Динамическая шкала

# Графические объекты
points_rk4 = ax1.scatter(x_rk4[0], v_rk4[0], c=np.linspace(0, 1, N), cmap='plasma', s=10)
points_dp8 = ax2.scatter(x_dp8[0], v_dp8[0], c=np.linspace(0, 1, N), cmap='plasma', s=10)
points_rk6 = ax3.scatter(x_rk6[0], v_rk6[0], c=np.linspace(0, 1, N), cmap='plasma', s=10)
line_x_rk4_dp8, = ax4.plot([], [], 'b-', label='Error in x (RK4)')
line_v_rk4_dp8, = ax4.plot([], [], 'r-', label='Error in v (RK4)')
line_x_rk6_dp8, = ax5.plot([], [], 'b-', label='Error in x (RK6)')
line_v_rk6_dp8, = ax5.plot([], [], 'r-', label='Error in v (RK6)')

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
    points_dp8.set_offsets(np.column_stack((x_dp8[frame], v_dp8[frame])))
    points_rk6.set_offsets(np.column_stack((x_rk6[frame], v_rk6[frame])))
    line_x_rk4_dp8.set_data(time[:frame + 1], avg_diff_x_rk4_dp8[:frame + 1])
    line_v_rk4_dp8.set_data(time[:frame + 1], avg_diff_v_rk4_dp8[:frame + 1])
    line_x_rk6_dp8.set_data(time[:frame + 1], avg_diff_x_rk6_dp8[:frame + 1])
    line_v_rk6_dp8.set_data(time[:frame + 1], avg_diff_v_rk6_dp8[:frame + 1])
    points_rk4.set_visible(True)
    points_dp8.set_visible(True)
    points_rk6.set_visible(True)
    line_x_rk4_dp8.set_visible(True)
    line_v_rk4_dp8.set_visible(True)
    line_x_rk6_dp8.set_visible(True)
    line_v_rk6_dp8.set_visible(True)
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
    points_dp8.set_offsets(np.column_stack((x_dp8[frame], v_dp8[frame])))
    points_rk6.set_offsets(np.column_stack((x_rk6[frame], v_rk6[frame])))
    line_x_rk4_dp8.set_data(time[:frame + 1], avg_diff_x_rk4_dp8[:frame + 1])
    line_v_rk4_dp8.set_data(time[:frame + 1], avg_diff_v_rk4_dp8[:frame + 1])
    line_x_rk6_dp8.set_data(time[:frame + 1], avg_diff_x_rk6_dp8[:frame + 1])
    line_v_rk6_dp8.set_data(time[:frame + 1], avg_diff_v_rk6_dp8[:frame + 1])
    slider.set_val(frame)
    return points_rk4, points_dp8, points_rk6, line_x_rk4_dp8, line_v_rk4_dp8, line_x_rk6_dp8, line_v_rk6_dp8

# Функция запуска анимации
def play(event):
    global anim
    if anim is None or anim.event_source is None:
        anim = animation.FuncAnimation(
            fig, animate, frames=range(current_frame, steps), interval=1, blit=False, repeat=True
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