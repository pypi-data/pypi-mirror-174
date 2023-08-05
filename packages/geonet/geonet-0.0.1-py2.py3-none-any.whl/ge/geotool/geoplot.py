from matplotlib import pyplot
from .geofigures import SIZE, set_limits, plot_coords, plot_bounds, plot_line_issimple

COLOR = {
    True: '#6699cc',
    False: '#ffcc33'
}


def v_color(ob):
    return COLOR[ob.is_simple]


def plot_coords(ax, ob):
    x, y = ob.xy
    ax.plot(x, y, 'o', color='#999999', zorder=1)


def plot_bounds(ax, ob):
    x, y = zip(*list((p.x, p.y) for p in ob.boundary))
    ax.plot(x, y, 'o', color='#000000', zorder=1)


def plot_line(ax, ob):
    x, y = ob.xy
    ax.plot(x, y, color=v_color(ob), alpha=0.7, linewidth=3, solid_capstyle='round', zorder=2)


def plot_linegroup(ax, linegroup):
    for plot_line in linegroup:
        # plot_coords(ax, plot_line)
        # plot_bounds(ax, plot_line)
        plot_line_issimple(ax, plot_line, alpha=0.7)


def plot_pointgroup(ax, pointgroup):
    for plot_point in pointgroup:
        plot_coords(ax, plot_point)


def plot_polygongroup(ax, polygongroup):
    for i in range(len(polygongroup.geoms)):
        x, y = polygongroup.geoms[i].exterior.xy
        ax.plot(x, y)


def multiple_plot(pointgroup=[], linegroup=[], polygongroup=[]):
    fig = pyplot.figure(1, figsize=SIZE, dpi=90)
    ax = fig.add_subplot(121)
    ax.set_title('a) simple')

    if len(pointgroup) > 0:
        plot_pointgroup(ax, pointgroup)
    if len(linegroup) > 0:
        plot_linegroup(ax, linegroup)
    if len(polygongroup) > 0:
        plot_polygongroup(ax, polygongroup)
    pyplot.show()
