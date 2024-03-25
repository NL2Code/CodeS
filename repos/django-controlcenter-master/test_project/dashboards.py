from controlcenter import Dashboard, widgets


class EmptyDashboard(Dashboard):
    pass


class MyWidget0(widgets.Widget):
    template_name = 'chart.html'


class MyWidget1(widgets.Widget):
    template_name = 'chart.html'


class NonEmptyDashboard(Dashboard):
    widgets = [
        MyWidget0,
        widgets.Group([MyWidget1])
    ]
