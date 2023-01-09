def init_3d_graphic():
    """
    Инициализирует матплотлибу. Возвращает объекты axes и plot.


    :return: AXES, PLOT
    """
    import matplotlib.pyplot as plt

    # нужный импорт для 3D моделирования
    from mpl_toolkits.mplot3d import Axes3D

    # noinspection PyStatementEffect
    Axes3D

    return plt.axes(projection='3d'), plt


def init_2d_graphic():
    """
    Инициализирует матплотлибу. Возвращает объект plot.


    :return: AXES, PLOT
    """
    import matplotlib.pyplot as plt
    plt.close()  # закроет другие открытые графики

    return plt


def build_surface(axes, x, y, z):
    """
    Строит фигуру в текущем пространстве axes


    :param axes: plt.axes(projection='3d') - Текущее просторанство
    :param x: numpy array
    :param y: numpy array
    :param z: numpy array
    """

    axes.plot_surface(x, y, z)
    # ax.plot_wireframe(X, Y, Z, rstride=1, cstride=1)

    axes.set_title('surface')
    axes.set_xlabel('x')
    axes.set_ylabel('y')
    axes.set_zlabel('z')


def build_main_surface(axes, plot_, x, y, z):
    """
        Графическое построение моделируемой поверхности

    :param axes:
    :param plot_:
    :param x:
    :param y:
    :param z:
    :return:
    """
    plot_.figure(1)
    axes.plot_surface(
        x, y, z, rstride=1, cstride=1,
        cmap='viridis',
        edgecolor='red',
        antialiased=True,
        alpha=0.5,
    )

    # Plot projections of the contours for each dimension.  By choosing offsets
    # that match the appropriate axes limits, the projected contours will sit on
    # the 'walls' of the graph
    # cset = ax.contour(X, Y, Z, zdir='z', offset=DOTS_COUNT, cmap=cm.coolwarm)
    # cset = ax.contour(X, Y, Z, zdir='x', offset=DOTS_COUNT, cmap=cm.coolwarm)
    # cset = ax.contour(X, Y, Z, zdir='y', offset=DOTS_COUNT, cmap=cm.coolwarm)

    axes.set_title('surface')
    axes.set_xlabel('x')
    axes.set_ylabel('y')
    axes.set_zlabel('z')
tablename=('Название таблицы')